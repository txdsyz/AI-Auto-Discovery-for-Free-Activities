'use client';

import { Event } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { Calendar, Users } from 'lucide-react';

interface EventCardProps {
  event: Event;
}

export function EventCard({ event }: EventCardProps) {
  return (
    <div className="rounded-lg border border-gray-200 p-4 bg-white hover:shadow-sm transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h4 className="font-semibold text-base">{event.name}</h4>
        <Badge
          className={
            event.type === 'recurring'
              ? 'bg-blue-500 text-white hover:bg-blue-600'
              : 'bg-green-500 text-white hover:bg-green-600'
          }
        >
          {event.type === 'recurring' ? 'Recurring' : 'One-time'}
        </Badge>
      </div>

      <div className="space-y-2 text-sm text-muted-foreground">
        {(event.schedule || event.date) && (
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            <span>{event.schedule || new Date(event.date!).toLocaleDateString('sv-SE')}</span>
          </div>
        )}
        
        {event.age_range && (
          <div className="flex items-center gap-2">
            <Users className="h-4 w-4" />
            <span>Ages {event.age_range}</span>
          </div>
        )}
      </div>

      {event.description && (
        <p className="mt-3 text-sm text-gray-600 leading-relaxed">{event.description}</p>
      )}
    </div>
  );
}
