import { useState, useEffect } from 'react';
import { BookSearch } from '@/components/books/BookSearch';
import { BookGrid } from '@/components/books/BookGrid';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { getBooks } from '@/services/api';
import { Book } from '@/types';
import { handleApiError } from '@/utils/errorHandling';

/**
 * Books page component with search and filtering
 */
export function Books() {
  const [books, setBooks] = useState<Book[]>([]);
  const [filteredBooks, setFilteredBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sortBy, setSortBy] = useState('title');
  const [selectedGenre, setSelectedGenre] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const booksPerPage = 16;

  useEffect(() => {
    loadBooks();
  }, []);

  const loadBooks = async () => {
    setIsLoading(true);
    try {
      const data = await getBooks();
      setBooks(data);
      setFilteredBooks(data);
    } catch (error) {
      handleApiError(error);
    } finally {
      setIsLoading(false);
    }
  };

  // Get unique genres
  const genres = ['all', ...Array.from(new Set(books.map((book) => book.genre)))];

  const applyFilters = (searchQuery = '', genre = selectedGenre) => {
    let filtered = books;

    // Filter by genre
    if (genre !== 'all') {
      filtered = filtered.filter((book) => book.genre === genre);
    }

    // Filter by search query
    if (searchQuery.trim()) {
      const lowercaseQuery = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (book) =>
          book.title.toLowerCase().includes(lowercaseQuery) ||
          book.author.toLowerCase().includes(lowercaseQuery) ||
          book.genre.toLowerCase().includes(lowercaseQuery)
      );
    }

    // Apply current sort
    filtered = sortBooks(filtered, sortBy);

    setFilteredBooks(filtered);
  };

  const sortBooks = (booksToSort: Book[], sortValue: string) => {
    return [...booksToSort].sort((a, b) => {
      switch (sortValue) {
        case 'title':
          return a.title.localeCompare(b.title);
        case 'author':
          return a.author.localeCompare(b.author);
        case 'rating':
          return b.rating - a.rating; // Highest first
        case 'year':
          return b.publishedYear - a.publishedYear; // Newest first
        default:
          return 0;
      }
    });
  };

  const handleSearch = (query: string) => {
    setCurrentPage(1); // Reset to first page on search
    applyFilters(query, selectedGenre);
  };

  const handleGenreChange = (genre: string) => {
    setCurrentPage(1); // Reset to first page on filter
    setSelectedGenre(genre);
    applyFilters('', genre);
  };

  const handleSort = (value: string) => {
    setSortBy(value);
    const sorted = sortBooks(filteredBooks, value);
    setFilteredBooks(sorted);
  };

  // Pagination logic
  const totalPages = Math.ceil(filteredBooks.length / booksPerPage);
  const startIndex = (currentPage - 1) * booksPerPage;
  const endIndex = startIndex + booksPerPage;
  const currentBooks = filteredBooks.slice(startIndex, endIndex);

  const goToPage = (page: number) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="container mx-auto">
        {/* Header */}
        <div className="mb-12 text-center">
          <h1 className="text-5xl md:text-6xl font-extrabold mb-4">
            <span className="gradient-text">Book Catalog</span>
          </h1>
          <p className="text-slate-600 text-xl">
            Browse our collection of{' '}
            <span className="font-bold text-violet-600">{books.length}</span> amazing books
          </p>
        </div>

        {/* Search */}
        <div className="mb-8">
          <BookSearch onSearch={handleSearch} />
        </div>

        {/* Filters & Sort */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div className="flex items-center gap-4">
            <div className="glass-effect px-4 py-2 rounded-xl border border-white/20">
              <p className="text-slate-700 font-semibold">
                Showing <span className="text-violet-600">{filteredBooks.length}</span>{' '}
                {filteredBooks.length === 1 ? 'book' : 'books'}
              </p>
            </div>

            {/* Genre Filter */}
            <div className="flex items-center gap-3">
              <label className="text-sm text-slate-700 font-semibold">Genre:</label>
              <select
                value={selectedGenre}
                onChange={(e) => handleGenreChange(e.target.value)}
                className="input-modern px-4 py-2.5 text-sm font-medium"
              >
                {genres.map((genre) => (
                  <option key={genre} value={genre}>
                    {genre === 'all' ? 'All Genres' : genre}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Sort */}
          <div className="flex items-center gap-3">
            <label className="text-sm text-slate-700 font-semibold">Sort by:</label>
            <select
              value={sortBy}
              onChange={(e) => handleSort(e.target.value)}
              className="input-modern px-4 py-2.5 text-sm font-medium"
            >
              <option value="title">Title</option>
              <option value="author">Author</option>
              <option value="rating">Rating</option>
              <option value="year">Year</option>
            </select>
          </div>
        </div>

        {/* Book Grid */}
        <BookGrid books={currentBooks} />

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="mt-12 flex justify-center">
            <div className="flex items-center gap-2">
              <button
                onClick={() => goToPage(currentPage - 1)}
                disabled={currentPage === 1}
                className="px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Previous
              </button>

              {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                <button
                  key={page}
                  onClick={() => goToPage(page)}
                  className={`px-4 py-2 rounded-lg font-medium transition-all ${
                    currentPage === page
                      ? 'bg-violet-600 text-white shadow-lg'
                      : 'bg-white border border-slate-200 text-slate-700 hover:bg-slate-50'
                  }`}
                >
                  {page}
                </button>
              ))}

              <button
                onClick={() => goToPage(currentPage + 1)}
                disabled={currentPage === totalPages}
                className="px-4 py-2 rounded-lg bg-white border border-slate-200 text-slate-700 font-medium hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                Next
              </button>
            </div>
          </div>
        )}

        {/* Results info */}
        <div className="mt-6 text-center text-slate-600">
          Showing {startIndex + 1}-{Math.min(endIndex, filteredBooks.length)} of{' '}
          {filteredBooks.length} books
        </div>
      </div>
    </div>
  );
}
