import { useNavigate } from 'react-router-dom';
import { Book } from '@/types';
import { formatRating } from '@/utils/formatters';
import { Button } from '@/components/common/Button';

/**
 * BookCard component props
 */
interface BookCardProps {
  book: Book;
}

/**
 * Modern BookCard with beautiful hover effects and gradients
 *
 * @example
 * <BookCard book={book} />
 */
export function BookCard({ book }: BookCardProps) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/books/${book.id}`);
  };

  // Generate placeholder based on genre
  const getPlaceholderColor = (genre: string) => {
    const colors: Record<string, string> = {
      Fiction: 'from-blue-400 to-blue-600',
      Mystery: 'from-purple-400 to-purple-600',
      Romance: 'from-pink-400 to-pink-600',
      'Science Fiction': 'from-cyan-400 to-cyan-600',
      Fantasy: 'from-violet-400 to-violet-600',
      Horror: 'from-red-400 to-red-600',
      'Non-Fiction': 'from-green-400 to-green-600',
    };
    return colors[genre] || 'from-gray-400 to-gray-600';
  };

  const placeholderUrl = `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='400'%3E%3Cdefs%3E%3ClinearGradient id='grad' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E%3Cstop offset='0%25' style='stop-color:%23${getPlaceholderColor(book.genre).includes('blue') ? '60a5fa' : getPlaceholderColor(book.genre).includes('purple') ? 'a78bfa' : getPlaceholderColor(book.genre).includes('pink') ? 'f472b6' : getPlaceholderColor(book.genre).includes('cyan') ? '22d3ee' : getPlaceholderColor(book.genre).includes('violet') ? '8b5cf6' : getPlaceholderColor(book.genre).includes('red') ? 'f87171' : '4ade80'};stop-opacity:1'/%3E%3Cstop offset='100%25' style='stop-color:%23${getPlaceholderColor(book.genre).includes('blue') ? '2563eb' : getPlaceholderColor(book.genre).includes('purple') ? '7c3aed' : getPlaceholderColor(book.genre).includes('pink') ? 'ec4899' : getPlaceholderColor(book.genre).includes('cyan') ? '0891b2' : getPlaceholderColor(book.genre).includes('violet') ? '6d28d9' : getPlaceholderColor(book.genre).includes('red') ? 'dc2626' : '16a34a'};stop-opacity:1'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect width='300' height='400' fill='url(%23grad)'/%3E%3Ctext x='50%25' y='45%25' font-family='Arial' font-size='24' fill='white' text-anchor='middle' font-weight='bold'%3E${encodeURIComponent(book.genre)}%3C/text%3E%3Ctext x='50%25' y='55%25' font-family='Arial' font-size='16' fill='white' text-anchor='middle' opacity='0.8'%3ENo Cover%3C/text%3E%3C/svg%3E`;

  return (
    <div
      className="glass-effect rounded-2xl overflow-hidden card-hover cursor-pointer group border border-white/20 hover-glow"
      onClick={handleClick}
    >
      <div className="relative overflow-hidden">
        <img
          src={book.coverImage}
          alt={book.title}
          className="w-full h-80 object-cover group-hover:scale-110 transition-transform duration-700"
          onError={(e) => {
            e.currentTarget.src = placeholderUrl;
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        <div className="absolute bottom-4 left-4 right-4 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-y-4 group-hover:translate-y-0">
          <Button
            variant="secondary"
            size="sm"
            className="w-full"
            onClick={(e) => {
              e.stopPropagation();
              handleClick();
            }}
          >
            View Details
          </Button>
        </div>

        {/* Floating Badge */}
        <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
          <div className="bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-full shadow-lg">
            <div className="flex items-center">
              <svg className="w-4 h-4 text-amber-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              <span className="text-sm font-bold text-slate-900">{formatRating(book.rating)}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="p-6">
        <h3 className="text-lg font-bold text-slate-900 mb-2 line-clamp-2 group-hover:text-violet-600 transition-colors">
          {book.title}
        </h3>
        <p className="text-sm text-slate-600 mb-4 font-medium">{book.author}</p>
        <div className="flex items-center justify-between">
          <span className="badge-modern">{book.genre}</span>
          <div className="flex items-center text-slate-500">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span className="text-xs font-medium">{book.publishedYear}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
