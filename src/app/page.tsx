'use client';

import { useState, useEffect } from 'react';
import { Navbar } from '@/components/navbar';
import { OrganizationsList } from '@/components/organizations-list';
import { OrganizationDetails } from '@/components/organization-details';
import { EventsList } from '@/components/events-list';
import { EventDetailsStandalone } from '@/components/event-details-standalone';
import { DiscoverSidebar } from '@/components/discover-sidebar';
import { BackendStatus } from '@/components/backend-status';
import { Organization, StandaloneEvent } from '@/lib/types';
import { api } from '@/lib/api';
import { mockOrganizations } from '@/lib/mock-data';

export default function Home() {
  const [activeView, setActiveView] = useState<'organizations' | 'events'>('organizations');
  
  // Organizations state
  const [organizations, setOrganizations] = useState<Organization[]>(mockOrganizations);
  const [selectedOrgId, setSelectedOrgId] = useState<string | null>(null);
  const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null);
  const [orgLoading, setOrgLoading] = useState(false);
  const [orgDetailsLoading, setOrgDetailsLoading] = useState(false);
  
  // Events state
  const [events, setEvents] = useState<StandaloneEvent[]>([]);
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
  const [selectedEvent, setSelectedEvent] = useState<StandaloneEvent | null>(null);
  const [eventsLoading, setEventsLoading] = useState(false);
  const [eventDetailsLoading, setEventDetailsLoading] = useState(false);
  
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Load organizations from API on mount
  useEffect(() => {
    if (activeView === 'organizations') {
      loadOrganizations();
    } else {
      loadEvents();
    }
  }, [activeView]);

  // Load selected organization details
  useEffect(() => {
    if (selectedOrgId) {
      loadOrganizationDetails(selectedOrgId);
    } else {
      setSelectedOrg(null);
    }
  }, [selectedOrgId]);

  // Load selected event details
  useEffect(() => {
    if (selectedEventId) {
      loadEventDetails(selectedEventId);
    } else {
      setSelectedEvent(null);
    }
  }, [selectedEventId]);

  const loadOrganizations = async () => {
    try {
      setOrgLoading(true);
      const data = await api.getOrganizations({ limit: 50 });
      if (data.organizations.length > 0) {
        setOrganizations(data.organizations);
      }
    } catch (error) {
      console.log('Backend not available, using mock data');
    } finally {
      setOrgLoading(false);
    }
  };

  const loadOrganizationDetails = async (id: string) => {
    try {
      setOrgDetailsLoading(true);
      const org = await api.getOrganization(id);
      setSelectedOrg(org);
    } catch (error) {
      console.log('Backend not available, using mock data for details');
      const mockOrg = organizations.find((o) => o.id === id);
      setSelectedOrg(mockOrg || null);
    } finally {
      setOrgDetailsLoading(false);
    }
  };

  const loadEvents = async () => {
    try {
      setEventsLoading(true);
      const data = await api.getEvents({ limit: 50 });
      setEvents(data.events);
    } catch (error) {
      console.error('Failed to load events:', error);
      setEvents([]);
    } finally {
      setEventsLoading(false);
    }
  };

  const loadEventDetails = async (id: string) => {
    try {
      setEventDetailsLoading(true);
      const event = await api.getEvent(id);
      setSelectedEvent(event);
    } catch (error) {
      console.error('Failed to load event details:', error);
      const fallbackEvent = events.find((e) => e.id === id);
      setSelectedEvent(fallbackEvent || null);
    } finally {
      setEventDetailsLoading(false);
    }
  };

  const handleSelectOrganization = (id: string) => {
    setSelectedOrgId(id);
  };

  const handleSelectEvent = (id: string) => {
    setSelectedEventId(id);
  };

  const handleDiscoveryComplete = () => {
    if (activeView === 'organizations') {
      loadOrganizations();
    } else {
      loadEvents();
    }
  };

  const handleOrgStatusUpdate = (orgId: string, newStatus: string) => {
    setOrganizations(prevOrgs =>
      prevOrgs.map(org =>
        org.id === orgId ? { ...org, status: newStatus as any } : org
      )
    );
    
    if (selectedOrg && selectedOrg.id === orgId) {
      setSelectedOrg({ ...selectedOrg, status: newStatus as any });
    }
  };

  const handleEventStatusUpdate = (eventId: string, newStatus: string) => {
    setEvents(prevEvents =>
      prevEvents.map(event =>
        event.id === eventId ? { ...event, status: newStatus as any } : event
      )
    );
    
    if (selectedEvent && selectedEvent.id === eventId) {
      setSelectedEvent({ ...selectedEvent, status: newStatus as any });
    }
  };

  return (
    <div className="h-screen flex flex-col">
      {/* Navigation */}
      <Navbar 
        onDiscoverClick={() => setSidebarOpen(true)}
        activeView={activeView}
        onViewChange={setActiveView}
      />
      
      {/* Backend Status Banner */}
      {/* <BackendStatus /> */}

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {activeView === 'organizations' ? (
          <>
            {/* Organizations List - 30% width */}
            <div className="w-[30%] min-w-[320px]">
              <OrganizationsList
                organizations={organizations}
                selectedOrgId={selectedOrgId}
                onSelectOrganization={handleSelectOrganization}
                loading={orgLoading}
              />
            </div>

            {/* Organization Details - 70% width */}
            <div className="flex-1">
              <OrganizationDetails
                organization={selectedOrg}
                loading={orgDetailsLoading}
                onStatusUpdate={handleOrgStatusUpdate}
              />
            </div>
          </>
        ) : (
          <>
            {/* Events List - 30% width */}
            <div className="w-[30%] min-w-[320px]">
              <EventsList
                events={events}
                selectedEventId={selectedEventId}
                onSelectEvent={handleSelectEvent}
                loading={eventsLoading}
              />
            </div>

            {/* Event Details - 70% width */}
            <div className="flex-1">
              <EventDetailsStandalone
                event={selectedEvent}
                loading={eventDetailsLoading}
                onStatusUpdate={handleEventStatusUpdate}
              />
            </div>
          </>
        )}
      </div>

      {/* Discover Sidebar */}
      <DiscoverSidebar
        open={sidebarOpen}
        onOpenChange={setSidebarOpen}
        onDiscoveryComplete={handleDiscoveryComplete}
      />
    </div>
  );
}
