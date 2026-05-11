'use client';

import { StandaloneEvent } from '@/lib/types';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MapPin, Calendar, Clock } from 'lucide-react';

interface EventCardProps {
  event: StandaloneEvent;
  isSelected: boolean;
  onClick: () => void;
}

const sportEmojis: Record<string, string> = {
  'basketball': '🏀',
  'soccer': '⚽',
  'football': '⚽',
  'swimming': '🏊',
  'tennis': '🎾',
  'volleyball': '🏐',
  'handball': '🤾',
  'hockey': '🏒',
  'running': '🏃',
  'cycling': '🚴',
  'skating': '⛸️',
  'martial arts': '🥋',
  'gymnastics': '🤸',
  'climbing': '🧗',
};

const getSportEmoji = (sport: string): string => {
  const lowerSport = sport.toLowerCase();
  return sportEmojis[lowerSport] || '🎯';
};

const statusColors: Record<string, string> = {
  pending: 'bg-blue-100 text-blue-700',
  verified: 'bg-green-100 text-green-700',
  archived: 'bg-gray-100 text-gray-700',
};

const statusLabels: Record<string, string> = {
  pending: 'Pending',
  verified: 'Verified',
  archived: 'Archived',
};

export function EventCardStandalone({ event, isSelected, onClick }: EventCardProps) {
  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return null;
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    } catch {
      return dateStr;
    }
  };

  const statusBorderColors = {
    pending: 'border-gray-200',
    verified: 'border-green-600',
    archived: 'border-gray-400',
  };

  const statusBarColors = {
    pending: 'bg-blue-500',
    verified: 'bg-green-600',
    archived: 'bg-gray-500',
  };

  return (
    <div
      onClick={onClick}
      className={`group relative cursor-pointer rounded-lg border bg-white p-4 transition-all duration-200 hover:shadow-lg hover:-translate-y-0.5 ${
        isSelected
          ? 'border-blue-500 shadow-md ring-2 ring-blue-100'
          : statusBorderColors[event.status]
      }`}
    >
      {/* Selection indicator bar */}
      {isSelected && (
        <div className={`absolute left-0 top-0 bottom-0 w-1 rounded-l-lg ${statusBarColors[event.status]}`} />
      )}

      {/* Event name with sport category */}
      <div className="flex items-center gap-2 mb-1">
        <h3 className="font-bold text-base line-clamp-1 text-gray-900">
          {event.title}
        </h3>
        <span className="text-gray-300 text-sm">|</span>
        <span className="inline-flex items-center gap-1 text-xs opacity-70 shrink-0">
          <span>{getSportEmoji(event.sport_category)}</span>
          <span className="font-medium text-gray-600 capitalize">{event.sport_category}</span>
        </span>
      </div>

      {/* Compact meta info in one line */}
      <div className="flex items-center gap-1.5 text-xs text-gray-600 flex-wrap">
        {/* Free badge */}
        {event.is_free && (
          <>
            <span className="font-medium text-green-700">Free</span>
            <span className="text-gray-300">•</span>
          </>
        )}

        {/* Location */}
        {event.location && (
          <>
            <span className="inline-flex items-center gap-1 opacity-70">
              <span className="text-gray-400">📍</span>
              <span className="line-clamp-1">{event.location}</span>
            </span>
          </>
        )}

        {/* Date & Time */}
        {event.date && (
          <>
            <span className="text-gray-300">•</span>
            <span className="opacity-70">
              {formatDate(event.date)}
              {event.time && ` • ${event.time}`}
            </span>
          </>
        )}
      </div>
    </div>
  );
}
