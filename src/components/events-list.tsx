'use client';

import { useState } from 'react';
import { StandaloneEvent } from '@/lib/types';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { EventCardStandalone } from './event-card-standalone';
import { Search } from 'lucide-react';

interface EventsListProps {
  events: StandaloneEvent[];
  selectedEventId: string | null;
  onSelectEvent: (id: string) => void;
  loading?: boolean;
}

export function EventsList({
  events,
  selectedEventId,
  onSelectEvent,
  loading
}: EventsListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'verified' | 'archived'>('all');

  const filteredEvents = events.filter((event) => {
    const matchesSearch = event.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         event.city.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         event.sport_category.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || event.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="h-full overflow-y-auto bg-gray-50 p-3 border-r">
      {/* Search Bar */}
      <div className="sticky top-0 mb-3 z-10 bg-gray-50 pb-2">
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search events..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-white text-sm"
          />
        </div>

        {/* Status Filter Buttons */}
        <div className="grid grid-cols-3 gap-2 mb-2">
          <Button
            size="sm"
            variant={statusFilter === 'all' ? 'default' : 'outline'}
            onClick={() => setStatusFilter('all')}
            className="col-span-2 text-xs h-8"
          >
            All
          </Button>
          <Button
            size="sm"
            variant={statusFilter === 'pending' ? 'default' : 'outline'}
            onClick={() => setStatusFilter('pending')}
            className={`text-xs h-8 ${
              statusFilter === 'pending' 
                ? 'bg-blue-600 hover:bg-blue-700' 
                : 'hover:bg-blue-50 hover:text-blue-700 hover:border-blue-300'
            }`}
          >
            ⏳ Pending
          </Button>
          <Button
            size="sm"
            variant={statusFilter === 'verified' ? 'default' : 'outline'}
            onClick={() => setStatusFilter('verified')}
            className={`text-xs h-8 ${
              statusFilter === 'verified' 
                ? 'bg-green-600 hover:bg-green-700' 
                : 'hover:bg-green-50 hover:text-green-700 hover:border-green-300'
            }`}
          >
            ✅ Verified
          </Button>
          <Button
            size="sm"
            variant={statusFilter === 'archived' ? 'default' : 'outline'}
            onClick={() => setStatusFilter('archived')}
            className={`col-span-2 text-xs h-8 ${
              statusFilter === 'archived' 
                ? 'bg-gray-600 hover:bg-gray-700' 
                : 'hover:bg-gray-50 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📦 Archived
          </Button>
        </div>

        {/* Count */}
        <p className="text-xs text-muted-foreground mb-2">
          {filteredEvents.length} event{filteredEvents.length !== 1 ? 's' : ''} found
        </p>
      </div>

      {/* Events List */}
      <div className="space-y-2">
        {filteredEvents.length === 0 ? (
          <div className="text-center py-12 px-4">
            <div className="text-4xl mb-3">📅</div>
            <p className="text-sm font-medium text-gray-900">No events found</p>
            <p className="text-xs text-muted-foreground mt-1">
              Try adjusting your search or filters
            </p>
          </div>
        ) : (
          filteredEvents.map((event) => (
            <EventCardStandalone
              key={event.id}
              event={event}
              isSelected={event.id === selectedEventId}
              onClick={() => onSelectEvent(event.id)}
            />
          ))
        )}
      </div>
    </div>
  );
}
