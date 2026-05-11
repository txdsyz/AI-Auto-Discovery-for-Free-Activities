'use client';

import { useState } from 'react';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { api } from '@/lib/api';
import { cn } from '@/lib/utils';

interface DiscoverSidebarProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onDiscoveryComplete: () => void;
}

type DiscoverTab = 'organizations' | 'events';

type SportCategory = 'basketball' | 'soccer' | 'swimming' | 'tennis' | 'volleyball' | 'handball' | 'hockey';

const SWEDISH_CITIES = [
  'Stockholm',
  'Göteborg',
  'Malmö',
  'Uppsala',
  'Västerås',
  'Örebro',
  'Linköping',
  'Helsingborg',
  'Jönköping',
  'Norrköping',
  'Lund',
  'Umeå',
  'Gävle',
  'Borås',
  'Södertälje',
];

export function DiscoverSidebar({ open, onOpenChange, onDiscoveryComplete }: DiscoverSidebarProps) {
  const [activeTab, setActiveTab] = useState<DiscoverTab>('organizations');
  const [searchQuery, setSearchQuery] = useState('');
  const [maxOrgs, setMaxOrgs] = useState(5);
  const [isDiscovering, setIsDiscovering] = useState(false);
  const [status, setStatus] = useState('');
  
  // Events discovery state
  const [eventCity, setEventCity] = useState('');
  const [showCityDropdown, setShowCityDropdown] = useState(false);
  const [eventActivity, setEventActivity] = useState('');
  const [showActivityDropdown, setShowActivityDropdown] = useState(false);
  const [maxEvents, setMaxEvents] = useState(10);
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');

  const handleRunDiscovery = async () => {
    if (!searchQuery.trim()) {
      setStatus('❌ Please enter a search query');
      return;
    }

    try {
      setIsDiscovering(true);
      setStatus('🔍 Running discovery... This may take 2-3 minutes');

      const result = await api.runDiscovery(searchQuery, maxOrgs);

      setStatus(
        `✅ Discovery complete!\n` +
        `Found ${result.organizations_found} organizations\n` +
        `Saved ${result.organizations_saved} organizations\n` +
        `Filtered ${result.irrelevant_filtered} irrelevant`
      );

      // Refresh the organizations list after a short delay
      setTimeout(() => {
        onDiscoveryComplete();
        onOpenChange(false);
      }, 3000);
    } catch (error) {
      console.error('Discovery failed:', error);
      setStatus('❌ Discovery failed. Please try again.');
    } finally {
      setIsDiscovering(false);
    }
  };

  const handleRunEventsDiscovery = async () => {
    if (!eventCity.trim()) {
      setStatus('❌ Please enter a city');
      return;
    }

    try {
      setIsDiscovering(true);
      setStatus('🔍 Running event discovery... This may take 2-3 minutes');

      const result = await api.runEventsDiscovery(eventCity, maxEvents);

      setStatus(
        `✅ Event discovery complete!\n` +
        `Events found: ${result.events_found}\n` +
        `Events saved: ${result.events_saved}`
      );

      // Refresh after a short delay
      setTimeout(() => {
        onDiscoveryComplete();
        onOpenChange(false);
      }, 3000);
    } catch (error) {
      console.error('Event discovery failed:', error);
      setStatus('❌ Event discovery failed. Please try again.');
    } finally {
      setIsDiscovering(false);
    }
  };

  const COMMON_ACTIVITIES = [
    '⚽ Football',
    '🏀 Basketball',
    '🏐 Volleyball',
    '🤾 Handball',
    '🏒 Hockey',
    '🎾 Tennis',
    '🏊 Swimming',
    '🏃 Running',
    '🚴 Cycling',
    '⛸️ Skating',
    '🥋 Martial Arts',
    '🤸 Gymnastics',
    '🧗 Climbing',
    '⚾ Baseball',
    '🏈 American Football',
    '🎮 Esports',
    '♟️ Chess',
    '🎨 Arts & Crafts',
    '🎭 Theater',
    '🎵 Music',
  ];

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent className="w-[600px] overflow-y-auto px-6 pt-4">
        <SheetHeader className="mb-1">
          <SheetTitle className="text-2xl">Discover</SheetTitle>
          <SheetDescription>
            Find new youth organizations and events
          </SheetDescription>
        </SheetHeader>

        {/* Tabs */}
        <div className="flex gap-2 mb-2">
          <Button
            variant={activeTab === 'organizations' ? 'default' : 'outline'}
            onClick={() => setActiveTab('organizations')}
            className="flex-1"
          >
            Organizations
          </Button>
          <Button
            variant={activeTab === 'events' ? 'default' : 'outline'}
            onClick={() => setActiveTab('events')}
            className="flex-1"
          >
            Events
          </Button>
        </div>

        {/* Organizations Tab Content */}
        {activeTab === 'organizations' && (
          <div className="space-y-6">
            {/* Search Query Input */}
            <div className="space-y-2">
              <Label htmlFor="searchQuery" className="text-sm font-semibold">
                Search Query
              </Label>
              <Input
                id="searchQuery"
                type="text"
                placeholder="e.g., Södermalm idrottsförening ungdom"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full"
              />
              <p className="text-xs text-muted-foreground">
                Enter a Swedish search query to find youth organizations
              </p>
              <div className="mt-3 p-3 bg-gray-50 rounded-lg space-y-1">
                <p className="text-xs font-medium text-gray-700">Example queries:</p>
                <p className="text-xs text-gray-600">• Södermalm idrottsförening ungdom</p>
                <p className="text-xs text-gray-600">• Stockholm ungdomsgård fritid</p>
                <p className="text-xs text-gray-600">• Kungsholmen scoutkår barn</p>
              </div>
            </div>

            {/* Max Organizations Input */}
            <div className="space-y-2">
              <Label htmlFor="maxOrgs" className="text-sm font-semibold">
                Maximum Organizations
              </Label>
              <Input
                id="maxOrgs"
                type="number"
                min={1}
                max={20}
                value={maxOrgs}
                onChange={(e) => setMaxOrgs(parseInt(e.target.value) || 5)}
                className="w-full"
              />
              <p className="text-xs text-muted-foreground">
                How many organizations to discover (1-20)
              </p>
            </div>

            {/* Run Discovery Button */}
            <Button
              onClick={handleRunDiscovery}
              disabled={isDiscovering || !searchQuery.trim()}
              className="w-full"
              size="lg"
            >
              {isDiscovering ? 'Running...' : 'Run Discovery'}
            </Button>

            {/* Status Display */}
            {status && (
              <div className="p-4 bg-blue-50 rounded-lg text-sm whitespace-pre-line">
                {status}
              </div>
            )}

            {/* Info Notes */}
            <div className="mt-2 space-y-2 text-xs text-muted-foreground">
              <p>⚠️ Discovery takes 2-3 minutes to complete</p>
              <p>💡 New organizations will appear in the list automatically</p>
            </div>
          </div>
        )}

        {/* Events Tab Content */}
        {activeTab === 'events' && (
          <div className="space-y-4">
            {/* City Input with Dropdown */}
            <div className="space-y-2 relative">
              <Label htmlFor="eventCity" className="text-sm font-medium">
                City/Location <span className="text-red-500">*</span>
              </Label>
              <div className="relative">
                <Input
                  id="eventCity"
                  type="text"
                  placeholder="Select or type a city..."
                  value={eventCity}
                  onChange={(e) => {
                    setEventCity(e.target.value);
                    setShowCityDropdown(true);
                  }}
                  onFocus={() => setShowCityDropdown(true)}
                  onBlur={() => setTimeout(() => setShowCityDropdown(false), 200)}
                  className="w-full"
                />
                {showCityDropdown && (
                  <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                    {SWEDISH_CITIES
                      .filter(city => 
                        city.toLowerCase().includes(eventCity.toLowerCase())
                      )
                      .map((city) => (
                        <button
                          key={city}
                          type="button"
                          onClick={() => {
                            setEventCity(city);
                            setShowCityDropdown(false);
                          }}
                          className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100 transition-colors"
                        >
                          {city}
                        </button>
                      ))}
                    {SWEDISH_CITIES.filter(city => 
                      city.toLowerCase().includes(eventCity.toLowerCase())
                    ).length === 0 && eventCity && (
                      <div className="px-3 py-2 text-sm text-gray-500 italic">
                        No matches - press Enter to use "{eventCity}"
                      </div>
                    )}
                  </div>
                )}
              </div>
              <p className="text-xs text-muted-foreground">
                Select from list or type any Swedish city name
              </p>
            </div>

            {/* Activity Category */}
            <div className="space-y-2 relative">
              <Label htmlFor="eventActivity" className="text-sm font-medium">
                Activity (Optional)
              </Label>
              <div className="relative">
                <Input
                  id="eventActivity"
                  type="text"
                  placeholder="Select or type an activity..."
                  value={eventActivity}
                  onChange={(e) => {
                    setEventActivity(e.target.value);
                    setShowActivityDropdown(true);
                  }}
                  onFocus={() => setShowActivityDropdown(true)}
                  onBlur={() => setTimeout(() => setShowActivityDropdown(false), 200)}
                  className="w-full"
                />
                {showActivityDropdown && (
                  <div className="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto">
                    {COMMON_ACTIVITIES
                      .filter(activity => 
                        activity.toLowerCase().includes(eventActivity.toLowerCase())
                      )
                      .map((activity) => (
                        <button
                          key={activity}
                          type="button"
                          onClick={() => {
                            setEventActivity(activity);
                            setShowActivityDropdown(false);
                          }}
                          className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100 transition-colors"
                        >
                          {activity}
                        </button>
                      ))}
                    {COMMON_ACTIVITIES.filter(activity => 
                      activity.toLowerCase().includes(eventActivity.toLowerCase())
                    ).length === 0 && eventActivity && (
                      <div className="px-3 py-2 text-sm text-gray-500 italic">
                        No matches - using "{eventActivity}"
                      </div>
                    )}
                  </div>
                )}
              </div>
              <p className="text-xs text-muted-foreground">
                Filter by specific activity or leave empty to search all
              </p>
            </div>

            {/* Date Range */}
            <div className="space-y-2">
              <Label className="text-sm font-medium">Date Range (Optional)</Label>
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <Label htmlFor="dateFrom" className="text-xs text-muted-foreground">From</Label>
                  <Input
                    id="dateFrom"
                    type="date"
                    value={dateFrom}
                    onChange={(e) => setDateFrom(e.target.value)}
                    className="w-full text-sm"
                  />
                </div>
                <div>
                  <Label htmlFor="dateTo" className="text-xs text-muted-foreground">To</Label>
                  <Input
                    id="dateTo"
                    type="date"
                    value={dateTo}
                    onChange={(e) => setDateTo(e.target.value)}
                    className="w-full text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Max Events */}
            <div className="space-y-2">
              <Label htmlFor="maxEvents" className="text-sm font-medium">
                Maximum Events: {maxEvents}
              </Label>
              <Input
                id="maxEvents"
                type="range"
                min={1}
                max={50}
                value={maxEvents}
                onChange={(e) => setMaxEvents(parseInt(e.target.value))}
                className="w-full"
              />
              <p className="text-xs text-muted-foreground">
                How many events to discover (1-50)
              </p>
            </div>

            {/* Run Discovery Button */}
            <Button
              onClick={handleRunEventsDiscovery}
              disabled={isDiscovering || !eventCity.trim()}
              className="w-full"
              size="lg"
            >
              {isDiscovering ? 'Running...' : 'Run Discovery'}
            </Button>

            {/* Status Display */}
            {status && (
              <div className="p-4 bg-blue-50 rounded-lg text-sm whitespace-pre-line">
                {status}
              </div>
            )}

            {/* Info Notes */}
            <div className="space-y-2 text-xs text-muted-foreground">
              <p className="font-medium text-gray-700">💡 Tips</p>
              <p>⚠️ Discovery takes 2-3 minutes to complete</p>
              <p>🎯 Try cities like: Uppsala, Stockholm, Göteborg</p>
              <p>🔍 Backend automatically generates bilingual search queries</p>
            </div>
          </div>
        )}
      </SheetContent>
    </Sheet>
  );
}
