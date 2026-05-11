'use client';

import { Organization } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface OrganizationCardProps {
  organization: Organization;
  isSelected: boolean;
  onClick: () => void;
}

const categoryColors = {
  sports: 'bg-blue-100 text-blue-700 hover:bg-blue-200',
  youth_centers: 'bg-green-100 text-green-700 hover:bg-green-200',
  scouts: 'bg-purple-100 text-purple-700 hover:bg-purple-200',
  cultural: 'bg-orange-100 text-orange-700 hover:bg-orange-200',
};

const categoryLabels = {
  sports: 'Sports',
  youth_centers: 'Youth Center',
  scouts: 'Scouts',
  cultural: 'Cultural',
};

const statusBorderColors = {
  pending: 'border-gray-200',
  background_check: 'border-yellow-600',
  onboarded: 'border-green-600',
  archived: 'border-gray-400',
};

const statusBarColors = {
  pending: 'bg-blue-500',
  background_check: 'bg-yellow-600',
  onboarded: 'bg-green-600',
  archived: 'bg-gray-500',
};

export function OrganizationCard({ organization, isSelected, onClick }: OrganizationCardProps) {
  const eventCount = organization.events?.length || 0;
  const status = organization.status || 'pending';
  
  // Get category icon
  const categoryIcons = {
    sports: '⚽',
    youth_centers: '🏢',
    scouts: '⛺',
    cultural: '🎨',
  };

  // Simplify location (remove "Stockholm" suffix if present)
  const displayLocation = organization.location?.replace(/, Stockholm$/, '').replace(' Stockholm', '') || 'Stockholm';

  return (
    <div
      onClick={onClick}
      className={cn(
        'group relative cursor-pointer rounded-lg border bg-white p-4 transition-all duration-200',
        'hover:shadow-lg hover:-translate-y-0.5',
        isSelected
          ? 'border-blue-500 shadow-md ring-2 ring-blue-100'
          : statusBorderColors[status]
      )}
    >
      {/* Selection indicator bar */}
      {isSelected && (
        <div className={cn(
          'absolute left-0 top-0 bottom-0 w-1 rounded-l-lg',
          statusBarColors[status]
        )} />
      )}

      {/* Organization name with category */}
      <div className="flex items-center gap-2 mb-1">
        <h3 className="font-bold text-base line-clamp-1 text-gray-900">
          {organization.name}
        </h3>
        <span className="text-gray-300 text-sm">|</span>
        <span className="inline-flex items-center gap-1 text-xs opacity-70 shrink-0">
          <span>{categoryIcons[organization.discovery.category]}</span>
          <span className="font-medium text-gray-600">{categoryLabels[organization.discovery.category]}</span>
        </span>
      </div>


      {/* Compact meta info in one line */}
      <div className="flex items-center gap-1.5 text-xs text-gray-600 flex-wrap">
        
        {/* Event count */}
        <span className="font-medium text-gray-700">
          {eventCount} {eventCount === 1 ? 'event' : 'events'}
        </span>

        {/* Location with icon */}
        {organization.location && (
          <>
            <span className="text-gray-300">•</span>
            <span className="inline-flex items-center gap-1 opacity-70">
              <span className="text-gray-400">📍</span>
              <span className="line-clamp-1">{displayLocation}</span>
            </span>
          </>
        )}
      </div>
    </div>
  );
}
