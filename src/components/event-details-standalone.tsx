'use client';

import { useState, useEffect } from 'react';
import { StandaloneEvent, EventStatus } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { MapPin, Calendar, Clock, Globe, ExternalLink, Archive } from 'lucide-react';
import { Separator } from '@/components/ui/separator';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { api } from '@/lib/api';

// Utility function to extract base URL for navigation
const getBaseUrlForHref = (url: string): string => {
  try {
    const urlObj = new URL(url);
    const protocol = urlObj.protocol;
    const hostname = urlObj.hostname;
    return `${protocol}//${hostname}`;
  } catch {
    return url;
  }
};

// Utility function to extract base URL for display
const getBaseUrl = (url: string): string => {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname.replace('www.', '');
  } catch {
    return url;
  }
};

interface EventDetailsProps {
  event: StandaloneEvent | null;
  loading?: boolean;
  onStatusUpdate?: (eventId: string, newStatus: EventStatus) => void;
}

const statusLabels: Record<EventStatus, string> = {
  pending: 'Pending',
  verified: 'Verified',
  archived: 'Archived',
};

const statusColors: Record<EventStatus, string> = {
  pending: 'bg-blue-100 text-blue-700',
  verified: 'bg-green-100 text-green-700',
  archived: 'bg-gray-100 text-gray-700',
};

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

export function EventDetailsStandalone({ event, loading, onStatusUpdate }: EventDetailsProps) {
  const [currentStatus, setCurrentStatus] = useState<EventStatus>(
    event?.status || 'pending'
  );

  // Update status when event changes
  useEffect(() => {
    if (event) {
      setCurrentStatus(event.status || 'pending');
    }
  }, [event?.id, event?.status]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center px-8">
        <div className="text-6xl mb-4">👈</div>
        <h3 className="text-xl font-semibold mb-2">Select an event</h3>
        <p className="text-muted-foreground">Choose from the list on the left to view details</p>
      </div>
    );
  }

  const handleStatusChange = async (newStatus: EventStatus) => {
    if (!event) return;
    
    try {
      setCurrentStatus(newStatus);
      await api.updateEventStatus(event.id, newStatus);
      console.log('✅ Status updated to:', newStatus);
      
      // Notify parent component to update the event list
      if (onStatusUpdate) {
        onStatusUpdate(event.id, newStatus);
      }
    } catch (error) {
      console.error('Failed to update status:', error);
      // Revert on error
      setCurrentStatus(event.status || 'pending');
      alert('Failed to update status. Please try again.');
    }
  };

  const handleArchive = () => {
    handleStatusChange('archived');
  };

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return null;
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('en-US', { 
        weekday: 'long',
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <div className="h-full overflow-y-auto bg-white p-8">
      {/* Event Header */}
      <div className="mb-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-4xl">{getSportEmoji(event.sport_category)}</span>
              <div>
                <h1 className="text-3xl font-bold mb-1">{event.title}</h1>
                <Badge className="capitalize">{event.sport_category}</Badge>
              </div>
            </div>
            {event.location && (
              <div className="flex items-center gap-2 text-muted-foreground mt-3">
                <MapPin className="h-4 w-4" />
                <span>{event.location}</span>
              </div>
            )}
          </div>

          {/* Status Management */}
          <div className="flex justify-end min-w-[280px]">
            {currentStatus !== 'archived' ? (
              <div className="grid grid-cols-2 gap-2 w-full">
                <Select
                  value={currentStatus}
                  onValueChange={(value) => handleStatusChange(value as EventStatus)}
                >
                  <SelectTrigger className={`w-full font-medium border-2 ${
                    currentStatus === 'pending' 
                      ? 'bg-blue-50 border-blue-300 text-blue-700 hover:bg-blue-100' 
                      : 'bg-green-50 border-green-300 text-green-700 hover:bg-green-100'
                  }`}>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="pending" className="text-blue-700">
                      <span className="flex items-center gap-2 font-medium">
                        ⏳ Pending
                      </span>
                    </SelectItem>
                    <SelectItem value="verified" className="text-green-700">
                      <span className="flex items-center gap-2 font-medium">
                        ✅ Verified
                      </span>
                    </SelectItem>
                  </SelectContent>
                </Select>
                <Button
                  variant="outline"
                  className="text-gray-600 hover:text-gray-900 hover:border-gray-400 border-2"
                  onClick={handleArchive}
                >
                  <Archive className="h-4 w-4 mr-2" />
                  Archive
                </Button>
              </div>
            ) : (
              <Badge className={`${statusColors[currentStatus]} px-4 py-2 text-sm justify-center`}>
                📦 Archived
              </Badge>
            )}
          </div>
        </div>
      </div>

      {/* Description */}
      <div className="mb-6">
        <p className="text-lg text-gray-700 leading-relaxed mb-3">
          {event.summary || event.description || 'No description available'}
        </p>
        {(event.source_url || event.url) && (
          <p className="text-sm text-muted-foreground">
            Source:{' '}
            <a
              href={event.source_url || event.url}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:underline text-blue-600"
            >
              {event.source_url || event.url}
            </a>
          </p>
        )}
      </div>

      <Separator className="my-6" />

      {/* Event Details */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Event Details</h2>
        <div className="space-y-3">
          {/* First Row: Date and Time */}
          {(event.date || event.time) && (
            <div className="grid grid-cols-2 gap-3">
              {event.date && (
                <div className="flex items-center gap-3 p-3 rounded-lg border bg-gray-50">
                  <Calendar className="h-5 w-5 text-primary shrink-0" />
                  <div>
                    <p className="text-xs text-muted-foreground">Date</p>
                    <p className="text-sm font-medium">{formatDate(event.date)}</p>
                  </div>
                </div>
              )}

              {event.time && (
                <div className="flex items-center gap-3 p-3 rounded-lg border bg-gray-50">
                  <Clock className="h-5 w-5 text-primary shrink-0" />
                  <div>
                    <p className="text-xs text-muted-foreground">Time</p>
                    <p className="text-sm font-medium">{event.time}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Second Row: City and Cost */}
          <div className="grid grid-cols-2 gap-3">
            <div className="flex items-center gap-3 p-3 rounded-lg border bg-gray-50">
              <MapPin className="h-5 w-5 text-primary shrink-0" />
              <div>
                <p className="text-xs text-muted-foreground">City</p>
                <p className="text-sm font-medium">{event.city}</p>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3 rounded-lg border bg-gray-50">
              <span className="text-xl shrink-0">{event.is_free ? '✓' : '💵'}</span>
              <div>
                <p className="text-xs text-muted-foreground">Cost</p>
                <p className="text-sm font-medium">{event.is_free ? 'Free' : 'Paid'}</p>
              </div>
            </div>
          </div>

          {/* Third Row: Age Group and Language */}
          {(event.age_group || event.language) && (
            <div className="grid grid-cols-2 gap-3">
              {event.age_group && (
                <div className="flex items-center gap-3 p-3 rounded-lg border bg-gray-50">
                  <span className="text-xl shrink-0">👥</span>
                  <div>
                    <p className="text-xs text-muted-foreground">Age Group</p>
                    <p className="text-sm font-medium">{event.age_group}</p>
                  </div>
                </div>
              )}

              {event.language && (
                <div className="flex items-center gap-3 p-3 rounded-lg border bg-gray-50">
                  <span className="text-xl shrink-0">🌐</span>
                  <div>
                    <p className="text-xs text-muted-foreground">Language</p>
                    <p className="text-sm font-medium">
                      {event.language === 'en' ? 'English' : 
                       event.language === 'sv' ? 'Swedish' : 
                       event.language.toUpperCase()}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Fourth Row: Website (full width) */}
          {(event.source_url || event.url) && (
            <a
              href={getBaseUrlForHref(event.source_url || event.url || '')}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 p-3 rounded-lg border hover:bg-gray-50 transition-colors hover:border-primary/50"
            >
              <Globe className="h-5 w-5 text-primary shrink-0" />
              <div className="flex-1">
                <p className="text-xs text-muted-foreground">Website</p>
                <p className="text-sm font-medium truncate">
                  {getBaseUrl(event.source_url || event.url || '')}
                </p>
              </div>
              <ExternalLink className="h-4 w-4 text-muted-foreground shrink-0" />
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
