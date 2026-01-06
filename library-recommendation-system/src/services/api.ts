import { Book, ReadingList, Review, Recommendation } from '@/types';
import { fetchAuthSession } from 'aws-amplify/auth';

/**
 * ============================================================================
 * API SERVICE LAYER - AWS BACKEND COMMUNICATION
 * ============================================================================
 *
 * Real AWS API implementation using:
 * - API Gateway endpoints
 * - Lambda functions
 * - DynamoDB for data storage
 * - Cognito for authentication
 * - Bedrock for AI recommendations
 *
 * ============================================================================
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

/**
 * Get authentication headers with Cognito JWT token
 */
async function getAuthHeaders(): Promise<Record<string, string>> {
  try {
    const session = await fetchAuthSession();
    const token = session.tokens?.idToken?.toString();
    return {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    };
  } catch {
    return {
      'Content-Type': 'application/json',
    };
  }
}

/**
 * Get all books from the catalog
 */
export async function getBooks(): Promise<Book[]> {
  const response = await fetch(`${API_BASE_URL}/books`);
  if (!response.ok) throw new Error('Failed to fetch books');
  return response.json();
}

/**
 * Get a single book by ID
 */
export async function getBook(id: string): Promise<Book | null> {
  const response = await fetch(`${API_BASE_URL}/books/${id}`);
  if (response.status === 404) return null;
  if (!response.ok) throw new Error('Failed to fetch book');
  return response.json();
}

/**
 * Create a new book (admin only)
 */
export async function createBook(book: Omit<Book, 'id'>): Promise<Book> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/books`, {
    method: 'POST',
    headers,
    body: JSON.stringify(book),
  });
  if (!response.ok) throw new Error('Failed to create book');
  return response.json();
}

/**
 * Update an existing book (admin only)
 */
export async function updateBook(id: string, book: Partial<Book>): Promise<Book> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/books/${id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(book),
  });
  if (!response.ok) throw new Error('Failed to update book');
  return response.json();
}

/**
 * Delete a book (admin only)
 */
export async function deleteBook(id: string): Promise<void> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/books/${id}`, {
    method: 'DELETE',
    headers,
  });
  if (!response.ok) throw new Error('Failed to delete book');
}

/**
 * Get AI-powered book recommendations using Amazon Bedrock
 */
export async function getRecommendations(query: string): Promise<Recommendation[]> {
  const headers = await getAuthHeaders();

  const response = await fetch(`${API_BASE_URL}/recommendations`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error('API Error Response:', errorText);
    throw new Error('Failed to get recommendations');
  }

  const data = await response.json();
  console.log('Raw API Response:', data);

  // Lambda returns { recommendations: [...] }
  const recommendations = data.recommendations || data || [];
  console.log('Parsed recommendations:', recommendations);

  // Add unique IDs and bookIds (AI doesn't return these)
  return recommendations.map(
    (
      rec: { title: string; author: string; reason: string; confidence: number },
      index: number
    ) => ({
      id: `rec-${Date.now()}-${index}`,
      bookId: `ai-${index}`, // Placeholder - AI recommendations don't match existing books
      reason: rec.reason,
      confidence: rec.confidence,
      title: rec.title,
      author: rec.author,
    })
  );
}

/**
 * Get user's reading lists
 */
export async function getReadingLists(): Promise<ReadingList[]> {
  const headers = await getAuthHeaders();

  // Get userId from JWT token
  const session = await fetchAuthSession();
  const userId = session.tokens?.idToken?.payload?.sub;

  if (!userId) {
    throw new Error('User not authenticated');
  }

  const response = await fetch(`${API_BASE_URL}/reading-lists?userId=${userId}`, {
    headers,
  });
  if (!response.ok) throw new Error('Failed to fetch reading lists');
  return response.json();
}

/**
 * Create a new reading list
 */
export async function createReadingList(
  list: Omit<ReadingList, 'id' | 'createdAt' | 'updatedAt'>
): Promise<ReadingList> {
  const headers = await getAuthHeaders();

  // Get userId from JWT token
  const session = await fetchAuthSession();
  const userId = session.tokens?.idToken?.payload?.sub;

  if (!userId) {
    throw new Error('User not authenticated');
  }

  const requestBody = {
    ...list,
    userId, // userId'yi ekle
  };

  const response = await fetch(`${API_BASE_URL}/reading-lists`, {
    method: 'POST',
    headers,
    body: JSON.stringify(requestBody),
  });
  if (!response.ok) throw new Error('Failed to create reading list');
  return response.json();
}

/**
 * Update a reading list
 */
export async function updateReadingList(
  id: string,
  list: Partial<ReadingList>
): Promise<ReadingList> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/reading-lists/${id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(list),
  });
  if (!response.ok) throw new Error('Failed to update reading list');
  return response.json();
}

/**
 * Delete a reading list
 */
export async function deleteReadingList(id: string): Promise<void> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/reading-lists/${id}`, {
    method: 'DELETE',
    headers,
  });
  if (!response.ok) throw new Error('Failed to delete reading list');
}

/**
 * Remove a book from a reading list
 */
export async function removeBookFromReadingList(
  listId: string,
  bookId: string
): Promise<ReadingList> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/reading-lists/${listId}/books/${bookId}`, {
    method: 'DELETE',
    headers,
  });
  if (!response.ok) throw new Error('Failed to remove book from reading list');
  return response.json();
}

/**
 * Get books by their IDs
 */
export async function getBooksByIds(bookIds: string[]): Promise<Book[]> {
  if (bookIds.length === 0) return [];

  // Mevcut /books endpoint'ini kullanarak tüm kitapları çek ve filtrele
  try {
    const allBooks = await getBooks();
    return allBooks.filter((book) => bookIds.includes(book.id));
  } catch (error) {
    console.error('Error fetching books by IDs:', error);
    throw new Error('Failed to fetch books');
  }
}

/**
 * Get reviews for a book
 */
export async function getReviews(bookId: string): Promise<Review[]> {
  const response = await fetch(`${API_BASE_URL}/books/${bookId}/reviews`);
  if (!response.ok) throw new Error('Failed to fetch reviews');
  return response.json();
}

/**
 * Create a new review
 */
export async function createReview(review: Omit<Review, 'id' | 'createdAt'>): Promise<Review> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/books/${review.bookId}/reviews`, {
    method: 'POST',
    headers,
    body: JSON.stringify(review),
  });
  if (!response.ok) throw new Error('Failed to create review');
  return response.json();
}
