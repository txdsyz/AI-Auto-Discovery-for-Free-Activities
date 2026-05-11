'use client';

import { useState } from 'react';
import { Organization } from '@/lib/types';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { OrganizationCard } from './organization-card';
import { Search } from 'lucide-react';

interface OrganizationsListProps {
  organizations: Organization[];
  selectedOrgId: string | null;
  onSelectOrganization: (id: string) => void;
  loading?: boolean;
}

export function OrganizationsList({
  organizations,
  selectedOrgId,
  onSelectOrganization,
  loading
}: OrganizationsListProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending' | 'background_check' | 'onboarded' | 'archived'>('all');

  const filteredOrganizations = organizations.filter((org) => {
    const matchesSearch = org.name.toLowerCase().includes(searchQuery.toLowerCase());
    // TODO: Filter by status once backend integration is complete
    const matchesStatus = statusFilter === 'all' || org.status === statusFilter;
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
      {/* Search Bar with count */}
      <div className="sticky top-0 mb-3 z-10 bg-gray-50 pb-2">
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search organizations..."
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
            variant={statusFilter === 'background_check' ? 'default' : 'outline'}
            onClick={() => setStatusFilter('background_check')}
            className={`text-xs h-8 ${
              statusFilter === 'background_check' 
                ? 'bg-yellow-600 hover:bg-yellow-700' 
                : 'hover:bg-yellow-50 hover:text-yellow-700 hover:border-yellow-300'
            }`}
          >
            🔍 Check
          </Button>
          <Button
            size="sm"
            variant={statusFilter === 'onboarded' ? 'default' : 'outline'}
            onClick={() => setStatusFilter('onboarded')}
            className={`text-xs h-8 ${
              statusFilter === 'onboarded' 
                ? 'bg-green-600 hover:bg-green-700' 
                : 'hover:bg-green-50 hover:text-green-700 hover:border-green-300'
            }`}
          >
            ✅ Onboarded
          </Button>
          <Button
            size="sm"
            variant={statusFilter === 'archived' ? 'default' : 'outline'}
            onClick={() => setStatusFilter('archived')}
            className={`text-xs h-8 ${
              statusFilter === 'archived' 
                ? 'bg-gray-600 hover:bg-gray-700' 
                : 'hover:bg-gray-50 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            📦 Archived
          </Button>
        </div>

        {filteredOrganizations.length > 0 && (
          <p className="text-xs text-gray-500 mt-2">
            Showing {filteredOrganizations.length} organization{filteredOrganizations.length !== 1 ? 's' : ''}
          </p>
        )}
      </div>

      {/* Organization Cards */}
      {filteredOrganizations.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📭</div>
          <h3 className="text-lg font-semibold mb-2">No organizations found</h3>
          <p className="text-sm text-muted-foreground">
            {searchQuery ? 'Try a different search term' : 'Click "Discover" to find organizations'}
          </p>
        </div>
      ) : (
        <div className="space-y-2">
          {filteredOrganizations.map((org) => (
            <OrganizationCard
              key={org.id}
              organization={org}
              isSelected={selectedOrgId === org.id}
              onClick={() => onSelectOrganization(org.id)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
