import { useState, useEffect } from 'react';
import { Button } from '@/components/common/Button';
import { Modal } from '@/components/common/Modal';
import { ConfirmDialog } from '@/components/common/ConfirmDialog';
import { Input } from '@/components/common/Input';
import { LoadingSpinner } from '@/components/common/LoadingSpinner';
import { BookCard } from '@/components/books/BookCard';
import {
  getReadingLists,
  createReadingList,
  getBooksByIds,
  deleteReadingList,
  removeBookFromReadingList,
} from '@/services/api';
import { ReadingList, Book } from '@/types';
import { formatDate } from '@/utils/formatters';
import { handleApiError } from '@/utils/errorHandling';
import { useToast } from '@/contexts/ToastContext';

/**
 * ReadingLists page component
 */
export function ReadingLists() {
  const { showToast } = useToast();
  const [lists, setLists] = useState<ReadingList[]>([]);
  const [selectedList, setSelectedList] = useState<ReadingList | null>(null);
  const [selectedListBooks, setSelectedListBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isBooksLoading, setIsBooksLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newListName, setNewListName] = useState('');
  const [newListDescription, setNewListDescription] = useState('');

  // Confirm dialog states
  const [confirmDialog, setConfirmDialog] = useState<{
    isOpen: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
  }>({
    isOpen: false,
    title: '',
    message: '',
    onConfirm: () => {},
  });

  useEffect(() => {
    loadLists();
  }, []);

  const loadLists = async () => {
    setIsLoading(true);
    try {
      const data = await getReadingLists();
      setLists(data);
    } catch (error) {
      handleApiError(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleListClick = async (list: ReadingList) => {
    setSelectedList(list);
    setIsBooksLoading(true);
    try {
      const books = await getBooksByIds(list.bookIds);
      setSelectedListBooks(books);
    } catch (error) {
      handleApiError(error);
      setSelectedListBooks([]);
    } finally {
      setIsBooksLoading(false);
    }
  };

  const handleBackToLists = () => {
    setSelectedList(null);
    setSelectedListBooks([]);
  };

  const handleDeleteList = async (listId: string, listName: string) => {
    setConfirmDialog({
      isOpen: true,
      title: 'Listeyi Sil',
      message: `"${listName}" reading listini silmek istediğinizden emin misiniz?`,
      onConfirm: async () => {
        try {
          await deleteReadingList(listId);
          setLists(lists.filter((list) => list.id !== listId));
          showToast('Reading list başarıyla silindi!', 'success');
        } catch (error) {
          handleApiError(error);
        }
      },
    });
  };

  const handleRemoveBookFromList = async (bookId: string, bookTitle: string) => {
    if (!selectedList) return;

    console.log('handleRemoveBookFromList called', bookId, bookTitle); // DEBUG

    const currentList = selectedList; // Closure için kaydet

    setConfirmDialog({
      isOpen: true,
      title: 'Kitabı Çıkar',
      message: `"${bookTitle}" kitabını bu listeden çıkarmak istediğinizden emin misiniz?`,
      onConfirm: async () => {
        console.log('Confirm clicked'); // DEBUG
        try {
          // Önce UI'ı güncelle (optimistic update)
          setSelectedListBooks((prevBooks) => prevBooks.filter((book) => book.id !== bookId));

          // Toast'u hemen göster
          showToast('Kitap listeden çıkarılıyor...', 'info');

          // API çağrısını yap
          const updatedList = await removeBookFromReadingList(currentList.id, bookId);

          // State'i güncelle
          setSelectedList(updatedList);

          // Ana liste state'ini de güncelle
          setLists((prevLists) =>
            prevLists.map((list) => (list.id === updatedList.id ? updatedList : list))
          );

          // Başarı mesajı
          showToast('Kitap listeden çıkarıldı!', 'success');
        } catch (error) {
          console.error('Error removing book:', error);
          // Hata durumunda kitabı geri ekle
          showToast('Kitap çıkarılamadı!', 'error');
          // Listeyi yeniden yükle
          if (currentList) {
            handleListClick(currentList);
          }
          handleApiError(error);
        }
      },
    });

    console.log('confirmDialog state set'); // DEBUG
  };

  const handleCreateList = async () => {
    if (!newListName.trim()) {
      showToast('Please enter a list name', 'warning');
      return;
    }

    try {
      const newList = await createReadingList({
        userId: '1', // TODO: Get from auth context
        name: newListName,
        description: newListDescription,
        bookIds: [],
      });
      setLists([...lists, newList]);
      setIsModalOpen(false);
      setNewListName('');
      setNewListDescription('');
      showToast('Reading list created successfully!', 'success');
    } catch (error) {
      handleApiError(error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Show individual reading list view
  if (selectedList) {
    return (
      <div className="min-h-screen py-8 px-4">
        <div className="container mx-auto">
          <div className="flex items-center mb-8">
            <Button variant="secondary" onClick={handleBackToLists} className="mr-4">
              ← Back to Lists
            </Button>
            <div>
              <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-2">
                {selectedList.name}
              </h1>
              <p className="text-slate-600 text-lg">{selectedList.description}</p>
              <p className="text-slate-500 text-sm mt-1">
                {selectedList.bookIds.length} books • Created {formatDate(selectedList.createdAt)}
              </p>
            </div>
          </div>

          {isBooksLoading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="lg" />
            </div>
          ) : selectedListBooks.length === 0 ? (
            <div className="text-center py-12 bg-white/90 backdrop-blur-sm rounded-xl shadow-lg border border-slate-200">
              <svg
                className="w-16 h-16 text-slate-400 mx-auto mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
              <h3 className="text-xl font-bold text-slate-900 mb-2">No books in this list yet</h3>
              <p className="text-slate-600 mb-4">
                Add books to this list by visiting book detail pages
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {selectedListBooks.map((book) => (
                <div key={book.id} className="relative group">
                  <div className="pointer-events-auto">
                    <BookCard book={book} />
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      handleRemoveBookFromList(book.id, book.title);
                    }}
                    className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full w-10 h-10 flex items-center justify-center shadow-lg transition-all z-[100] opacity-0 group-hover:opacity-100 group-hover:scale-110"
                    title="Listeden çıkar"
                    style={{ pointerEvents: 'auto' }}
                  >
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <ConfirmDialog
          isOpen={confirmDialog.isOpen}
          onClose={() => setConfirmDialog({ ...confirmDialog, isOpen: false })}
          onConfirm={confirmDialog.onConfirm}
          title={confirmDialog.title}
          message={confirmDialog.message}
          confirmText="Evet, Sil"
          cancelText="İptal"
          confirmVariant="danger"
        />
      </div>
    );
  }

  // Show reading lists overview
  return (
    <div className="min-h-screen py-8 px-4">
      <div className="container mx-auto">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-2">My Reading Lists</h1>
            <p className="text-slate-600 text-lg">Organize your books into custom lists</p>
          </div>
          <Button variant="primary" size="lg" onClick={() => setIsModalOpen(true)}>
            Create New List
          </Button>
        </div>

        {lists.length === 0 ? (
          <div className="text-center py-12 bg-white/90 backdrop-blur-sm rounded-xl shadow-lg border border-slate-200">
            <svg
              className="w-16 h-16 text-slate-400 mx-auto mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <h3 className="text-xl font-bold text-slate-900 mb-2">No reading lists yet</h3>
            <p className="text-slate-600 mb-4">
              Create your first list to start organizing your books
            </p>
            <Button variant="primary" onClick={() => setIsModalOpen(true)}>
              Create Your First List
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {lists.map((list) => (
              <div
                key={list.id}
                className="bg-white/90 backdrop-blur-sm rounded-xl shadow-sm border border-slate-200 p-6 hover:shadow-xl hover:border-blue-300 transition-all duration-300 relative group"
              >
                <div className="cursor-pointer" onClick={() => handleListClick(list)}>
                  <h3 className="text-xl font-bold text-slate-900 mb-2">{list.name}</h3>
                  <p className="text-slate-600 mb-4 line-clamp-2">{list.description}</p>
                  <div className="flex items-center justify-between text-sm text-slate-500">
                    <span>{list.bookIds.length} books</span>
                    <span>Created {formatDate(list.createdAt)}</span>
                  </div>
                </div>

                {/* Delete Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleDeleteList(list.id, list.name);
                  }}
                  className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 bg-red-500 hover:bg-red-600 text-white rounded-full w-8 h-8 flex items-center justify-center shadow-lg transition-all z-10"
                  title="Listeyi sil"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>
            ))}
          </div>
        )}

        <Modal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          title="Create New Reading List"
        >
          <div>
            <Input
              label="List Name"
              type="text"
              value={newListName}
              onChange={(e) => setNewListName(e.target.value)}
              placeholder="e.g., Summer Reading 2024"
              required
            />

            <div className="mb-4">
              <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
              <textarea
                value={newListDescription}
                onChange={(e) => setNewListDescription(e.target.value)}
                placeholder="What's this list about?"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 min-h-[100px] resize-none"
              />
            </div>

            <div className="flex gap-3">
              <Button variant="primary" onClick={handleCreateList} className="flex-1">
                Create List
              </Button>
              <Button variant="secondary" onClick={() => setIsModalOpen(false)} className="flex-1">
                Cancel
              </Button>
            </div>
          </div>
        </Modal>
      </div>

      <ConfirmDialog
        isOpen={confirmDialog.isOpen}
        onClose={() => setConfirmDialog({ ...confirmDialog, isOpen: false })}
        onConfirm={confirmDialog.onConfirm}
        title={confirmDialog.title}
        message={confirmDialog.message}
        confirmText="Evet, Sil"
        cancelText="İptal"
        confirmVariant="danger"
      />
    </div>
  );
}
