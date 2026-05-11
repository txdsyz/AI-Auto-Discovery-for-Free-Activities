'use client';

import { Button } from '@/components/ui/button';
import { Search } from 'lucide-react';

interface NavbarProps {
  onDiscoverClick: () => void;
  activeView: 'organizations' | 'events';
  onViewChange: (view: 'organizations' | 'events') => void;
}

export function Navbar({ onDiscoverClick, activeView, onViewChange }: NavbarProps) {
  return (
    <nav className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="flex h-16 w-full items-center justify-between px-6">
        <div className="flex items-center gap-6">
          {/* Logo/Brand */}
          <div className="flex items-center gap-2">
            <span className="text-2xl">🎓</span>
            <h1 className="text-xl font-bold bg-linear-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AfterClass
            </h1>
          </div>

          {/* Navigation Items */}
          <div className="flex items-center gap-6">
            <Button 
              variant="ghost" 
              className={`font-medium ${activeView === 'organizations' ? 'text-primary' : 'text-muted-foreground'}`}
              onClick={() => onViewChange('organizations')}
            >
              Organizations
            </Button>
            <Button 
              variant="ghost" 
              className={`font-medium ${activeView === 'events' ? 'text-primary' : 'text-muted-foreground'}`}
              onClick={() => onViewChange('events')}
            >
              Events
            </Button>
          </div>
        </div>

        {/* Discover Button - Right aligned */}
        <Button onClick={onDiscoverClick} className="gap-2">
          <Search className="h-4 w-4" />
          Discover
        </Button>
      </div>
    </nav>
  );
}
