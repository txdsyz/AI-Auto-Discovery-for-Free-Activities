import { Organization, OrganizationsResponse, DiscoveryResult, OrganizationStatus } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class AfterClassAPI {
  async getOrganizations(params: {
    limit?: number;
    offset?: number;
    category?: 'sports' | 'youth_centers' | 'scouts' | 'cultural';
    status?: OrganizationStatus;
  } = {}): Promise<OrganizationsResponse> {
    const { limit = 50, offset = 0, category, status } = params;
    
    let url = `${API_URL}/organizations?limit=${limit}&offset=${offset}`;
    if (category) {
      url += `&category=${category}`;
    }
    if (status) {
      url += `&status=${status}`;
    }
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch organizations: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async getOrganization(id: string): Promise<Organization> {
    const response = await fetch(`${API_URL}/organizations/${id}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Organization not found');
      }
      throw new Error(`Failed to fetch organization: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async runDiscovery(
    searchQuery: string,
    maxOrganizations: number = 5
  ): Promise<DiscoveryResult> {
    const response = await fetch(`${API_URL}/discover`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        search_query: searchQuery,
        max_organizations: maxOrganizations
      })
    });
    
    if (!response.ok) {
      throw new Error(`Discovery failed: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async updateOrganizationStatus(
    organizationId: string,
    status: OrganizationStatus
  ): Promise<{ success: boolean; new_status: string }> {
    const response = await fetch(`${API_URL}/organizations/${organizationId}/status`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to update organization status: ${response.statusText}`);
    }
    
    return response.json();
  }

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${API_URL}/health`);
    return response.json();
  }

  async runEventsDiscovery(
    city: string,
    maxEvents: number = 10
  ): Promise<{
    run_id: string;
    status: string;
    city: string;
    events_found: number;
    events_saved: number;
    started_at: string;
    completed_at: string;
  }> {
    const response = await fetch(`${API_URL}/events/discover`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        city: city,
        max_events: maxEvents
      })
    });
    
    if (!response.ok) {
      throw new Error(`Events discovery failed: ${response.statusText}`);
    }
    
    return response.json();
  }

  async getEvents(params: {
    limit?: number;
    offset?: number;
    city?: string;
    status?: string;
    sport_category?: string;
    date_from?: string;
    date_to?: string;
  } = {}): Promise<import('./types').EventsResponse> {
    const { limit = 50, offset = 0, city, status, sport_category, date_from, date_to } = params;
    
    let url = `${API_URL}/events?limit=${limit}&offset=${offset}`;
    if (city) url += `&city=${city}`;
    if (status) url += `&status=${status}`;
    if (sport_category) url += `&sport_category=${sport_category}`;
    if (date_from) url += `&date_from=${date_from}`;
    if (date_to) url += `&date_to=${date_to}`;
    
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Failed to fetch events: ${response.statusText}`);
    }
    
    return response.json();
  }

  async getEvent(id: string): Promise<import('./types').StandaloneEvent> {
    const response = await fetch(`${API_URL}/events/${id}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Event not found');
      }
      throw new Error(`Failed to fetch event: ${response.statusText}`);
    }
    
    return response.json();
  }

  async updateEventStatus(
    eventId: string,
    status: import('./types').EventStatus
  ): Promise<{ success: boolean; new_status: string }> {
    const response = await fetch(`${API_URL}/events/${eventId}/status`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ status })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to update event status: ${response.statusText}`);
    }
    
    return response.json();
  }

  async deleteEvent(eventId: string): Promise<void> {
    const response = await fetch(`${API_URL}/events/${eventId}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error(`Failed to delete event: ${response.statusText}`);
    }
  }
}

export const api = new AfterClassAPI();
