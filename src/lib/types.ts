export type OrganizationStatus = 'pending' | 'background_check' | 'onboarded' | 'archived';

export interface Organization {
  id: string;
  name: string;
  type: string;
  location: string | null;
  description: string;
  contact: {
    email: string | null;
    phone: string | null;
  };
  website: string;
  discovery: {
    category: 'sports' | 'youth_centers' | 'scouts' | 'cultural';
    search_query: string;
    search_score?: number;
    discovered_at?: string;
  };
  status?: OrganizationStatus;
  events?: Event[];
  created_at?: string;
  last_updated?: string;
}

export interface Event {
  id: string;
  organization_id: string;
  name: string;
  type: 'recurring' | 'one-time';
  schedule: string | null;
  date: string | null;
  age_range: string | null;
  description: string;
  created_at?: string;
}

export interface OrganizationsResponse {
  organizations: Organization[];
  total: number;
  limit: number;
  offset: number;
}

export interface DiscoveryResult {
  run_id: string;
  status: string;
  organizations_found: number;
  organizations_saved: number;
  irrelevant_filtered: number;
  started_at: string;
  completed_at: string;
}

// Standalone Events Types
export type EventStatus = 'pending' | 'verified' | 'archived';

export interface StandaloneEvent {
  id: string;
  title: string;
  description?: string;
  summary?: string;
  location: string | null;
  city: string;
  date: string | null;
  time: string | null;
  sport_category: string;
  is_free: boolean;
  url?: string;
  source_url?: string;
  status: EventStatus;
  age_group?: string;
  language?: string;
  _fallback?: boolean;
  created_at: string;
  last_updated: string;
}

export interface EventsResponse {
  events: StandaloneEvent[];
  total: number;
  limit: number;
  offset: number;
}
