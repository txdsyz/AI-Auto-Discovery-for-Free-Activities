'use client';

import { useState, useEffect } from 'react';
import { Organization, OrganizationStatus } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { EventCard } from './event-card';
import { Mail, Phone, Globe, MapPin, ExternalLink, Archive } from 'lucide-react';
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

interface OrganizationDetailsProps {
  organization: Organization | null;
  loading?: boolean;
  onStatusUpdate?: (orgId: string, newStatus: OrganizationStatus) => void;
}

const statusLabels: Record<OrganizationStatus, string> = {
  pending: 'Pending',
  background_check: 'Background Check',
  onboarded: 'Onboarded',
  archived: 'Archived',
};

const statusColors: Record<OrganizationStatus, string> = {
  pending: 'bg-blue-100 text-blue-700',
  background_check: 'bg-yellow-100 text-yellow-700',
  onboarded: 'bg-green-100 text-green-700',
  archived: 'bg-gray-100 text-gray-700',
};

export function OrganizationDetails({ organization, loading, onStatusUpdate }: OrganizationDetailsProps) {
  const [currentStatus, setCurrentStatus] = useState<OrganizationStatus>(
    organization?.status || 'pending'
  );

  // Update status when organization changes
  useEffect(() => {
    if (organization) {
      setCurrentStatus(organization.status || 'pending');
    }
  }, [organization?.id, organization?.status]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!organization) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center px-8">
        <div className="text-6xl mb-4">👈</div>
        <h3 className="text-xl font-semibold mb-2">Select an organization</h3>
        <p className="text-muted-foreground">Choose from the list on the left to view details</p>
      </div>
    );
  }

  const handleStatusChange = async (newStatus: OrganizationStatus) => {
    if (!organization) return;
    
    try {
      setCurrentStatus(newStatus);
      await api.updateOrganizationStatus(organization.id, newStatus);
      console.log('✅ Status updated to:', newStatus);
      
      // Notify parent component to update the organization list
      if (onStatusUpdate) {
        onStatusUpdate(organization.id, newStatus);
      }
    } catch (error) {
      console.error('Failed to update status:', error);
      // Revert on error
      setCurrentStatus(organization.status || 'pending');
      alert('Failed to update status. Please try again.');
    }
  };

  const handleArchive = () => {
    handleStatusChange('archived');
  };

  return (
    <div className="h-full overflow-y-auto bg-white p-8">
      {/* Organization Header */}
      <div className="mb-6">
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h1 className="text-3xl font-bold mb-2">{organization.name}</h1>
            <Badge className="mb-3">{organization.type}</Badge>
            {organization.location && (
              <div className="flex items-center gap-2 text-muted-foreground">
                <MapPin className="h-4 w-4" />
                <span>{organization.location}</span>
              </div>
            )}
          </div>

          {/* Status Management */}
          <div className="flex justify-end min-w-[280px]">
            {currentStatus !== 'archived' ? (
              <div className="grid grid-cols-2 gap-2 w-full">
                <Select
                  value={currentStatus}
                  onValueChange={(value) => handleStatusChange(value as OrganizationStatus)}
                >
                  <SelectTrigger className={`w-full font-medium border-2 ${
                    currentStatus === 'pending' 
                      ? 'bg-blue-50 border-blue-300 text-blue-700 hover:bg-blue-100' 
                      : currentStatus === 'background_check'
                      ? 'bg-yellow-50 border-yellow-300 text-yellow-700 hover:bg-yellow-100'
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
                    <SelectItem value="background_check" className="text-yellow-700">
                      <span className="flex items-center gap-2 font-medium">
                        🔍 Background Check
                      </span>
                    </SelectItem>
                    <SelectItem value="onboarded" className="text-green-700">
                      <span className="flex items-center gap-2 font-medium">
                        ✅ Onboarded
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
        <p className="text-lg text-gray-700 leading-relaxed mb-3">{organization.description}</p>
        <p className="text-sm text-muted-foreground">
          Source: <a href={organization.website} target="_blank" rel="noopener noreferrer" className="hover:underline text-blue-600">{organization.website}</a>
        </p>
      </div>

      <Separator className="my-6" />

      {/* Contact Information */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Contact Information</h2>
        <div className="grid grid-cols-2 gap-3">
          {organization.contact.email && (
            <a
              href={`mailto:${organization.contact.email}`}
              className="flex items-center gap-3 p-3 rounded-lg border hover:bg-gray-50 transition-colors hover:border-primary/50"
            >
              <Mail className="h-5 w-5 text-primary shrink-0" />
              <span className="text-sm truncate">{organization.contact.email}</span>
            </a>
          )}

          {organization.contact.phone && (
            <a
              href={`tel:${organization.contact.phone}`}
              className="flex items-center gap-3 p-3 rounded-lg border hover:bg-gray-50 transition-colors hover:border-primary/50"
            >
              <Phone className="h-5 w-5 text-primary shrink-0" />
              <span className="text-sm">{organization.contact.phone}</span>
            </a>
          )}

          <a
            href={getBaseUrlForHref(organization.website)}
            target="_blank"
            rel="noopener noreferrer"
            className={`flex items-center gap-3 p-3 rounded-lg border hover:bg-gray-50 transition-colors hover:border-primary/50 ${
              (!organization.contact.email && !organization.contact.phone) || 
              (organization.contact.email && organization.contact.phone) 
                ? 'col-span-2' 
                : ''
            }`}
          >
            <Globe className="h-5 w-5 text-primary shrink-0" />
            <span className="text-sm flex-1 truncate">{getBaseUrl(organization.website)}</span>
            <ExternalLink className="h-4 w-4 text-muted-foreground shrink-0" />
          </a>

          {!organization.contact.email && !organization.contact.phone && (
            <p className="col-span-2 text-sm text-muted-foreground italic text-center py-2">
              Contact information not available
            </p>
          )}
        </div>
      </div>

      <Separator className="my-6" />

      {/* Events Section */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Events</h2>
        {organization.events && organization.events.length > 0 ? (
          <div className="space-y-3">
            {organization.events.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        ) : (
          <p className="text-muted-foreground">No events listed for this organization</p>
        )}
      </div>
    </div>
  );
}
