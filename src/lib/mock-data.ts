import { Organization } from './types';

export const mockOrganizations: Organization[] = [
  // {
  //   id: '1',
  //   name: 'Södermalms Volleybollklubb',
  //   type: 'Sports Club',
  //   location: 'Södermalm, Stockholm',
  //   description: 'A vibrant volleyball club offering training for youth ages 7-19. We focus on both competitive and recreational volleyball with professional coaches and a welcoming community atmosphere.',
  //   contact: {
  //     email: 'info@sodervoll.se',
  //     phone: '070-123 45 67'
  //   },
  //   website: 'https://sodervoll.se',
  //   discovery: {
  //     category: 'sports',
  //     search_query: 'Södermalm volleyboll ungdom'
  //   },
  //   events: [
  //     {
  //       id: 'e1',
  //       organization_id: '1',
  //       name: 'Youth Training - Ages 7-12',
  //       type: 'recurring',
  //       schedule: 'Mondays and Wednesdays, 17:00-18:30',
  //       date: null,
  //       age_range: '7-12',
  //       description: 'Basic volleyball skills, fun games, and teamwork exercises for younger players'
  //     },
  //     {
  //       id: 'e2',
  //       organization_id: '1',
  //       name: 'Advanced Training - Ages 13-19',
  //       type: 'recurring',
  //       schedule: 'Tuesdays and Thursdays, 18:00-20:00',
  //       date: null,
  //       age_range: '13-19',
  //       description: 'Competitive training for experienced players with tournament preparation'
  //     },
  //     {
  //       id: 'e3',
  //       organization_id: '1',
  //       name: 'Summer Tournament 2025',
  //       type: 'one-time',
  //       schedule: null,
  //       date: '2025-07-15',
  //       age_range: '10-16',
  //       description: 'Annual summer volleyball tournament with teams from across Stockholm'
  //     }
  //   ]
  // },
  // {
  //   id: '2',
  //   name: 'IF Söderkamraterna',
  //   type: 'Sports Club',
  //   location: 'Södermalm, Stockholm',
  //   description: 'Football club for youth with teams from age 6 to 19. We emphasize teamwork, skill development, and having fun while learning the beautiful game.',
  //   contact: {
  //     email: 'info@soderkamraterna.se',
  //     phone: '070-742 59 22'
  //   },
  //   website: 'https://soderkamraterna.se',
  //   discovery: {
  //     category: 'sports',
  //     search_query: 'Södermalm fotboll barn'
  //   },
  //   events: [
  //     {
  //       id: 'e4',
  //       organization_id: '2',
  //       name: 'Training - F13 Team',
  //       type: 'recurring',
  //       schedule: 'Tuesdays and Thursdays, 18:00-19:30',
  //       date: null,
  //       age_range: '13',
  //       description: 'Football training for 13-year-olds focusing on tactics and teamwork'
  //     },
  //     {
  //       id: 'e5',
  //       organization_id: '2',
  //       name: 'Training - F09 Team',
  //       type: 'recurring',
  //       schedule: 'Saturdays, 10:00-11:30',
  //       date: null,
  //       age_range: '9',
  //       description: 'Fun football training for 9-year-olds with focus on basic skills'
  //     }
  //   ]
  // },
  // {
  //   id: '3',
  //   name: 'Kungsholmens Fritidsgård',
  //   type: 'Youth Center',
  //   location: 'Kungsholmen, Stockholm',
  //   description: 'Open youth center with activities, workshops, and a safe space for teenagers to hang out. Free entrance and open to everyone aged 13-19.',
  //   contact: {
  //     email: 'info@kungsholmensfg.se',
  //     phone: null
  //   },
  //   website: 'https://kungsholmensfg.se',
  //   discovery: {
  //     category: 'youth_centers',
  //     search_query: 'Kungsholmen fritidsgård'
  //   },
  //   events: [
  //     {
  //       id: 'e6',
  //       organization_id: '3',
  //       name: 'Open House',
  //       type: 'recurring',
  //       schedule: 'Monday-Friday, 15:00-20:00',
  //       date: null,
  //       age_range: '13-19',
  //       description: 'Drop-in activities including games, music studio, and hang-out areas'
  //     },
  //     {
  //       id: 'e7',
  //       organization_id: '3',
  //       name: 'Music Workshop',
  //       type: 'recurring',
  //       schedule: 'Wednesdays, 17:00-19:00',
  //       date: null,
  //       age_range: '13-19',
  //       description: 'Learn to play instruments and produce music with professional guidance'
  //     }
  //   ]
  // },
  // {
  //   id: '4',
  //   name: 'Vasastan Scoutkår',
  //   type: 'Scout Group',
  //   location: 'Vasastan, Stockholm',
  //   description: 'Traditional scout group offering outdoor activities, camping trips, and personal development for youth. Part of Svenska Scoutförbundet.',
  //   contact: {
  //     email: 'kontakt@vasastanscout.se',
  //     phone: '070-555 12 34'
  //   },
  //   website: 'https://vasastanscout.se',
  //   discovery: {
  //     category: 'scouts',
  //     search_query: 'Vasastan scout ungdom'
  //   },
  //   events: [
  //     {
  //       id: 'e8',
  //       organization_id: '4',
  //       name: 'Weekly Scout Meetings',
  //       type: 'recurring',
  //       schedule: 'Thursdays, 18:00-20:00',
  //       date: null,
  //       age_range: '7-18',
  //       description: 'Regular scout activities including games, skills training, and planning'
  //     },
  //     {
  //       id: 'e9',
  //       organization_id: '4',
  //       name: 'Summer Camp 2025',
  //       type: 'one-time',
  //       schedule: null,
  //       date: '2025-07-20',
  //       age_range: '10-16',
  //       description: 'Week-long summer camp with outdoor activities, camping, and adventures'
  //     }
  //   ]
  // },
  // {
  //   id: '5',
  //   name: 'Kulturhuset Ungdom',
  //   type: 'Cultural Center',
  //   location: 'Norrmalm, Stockholm',
  //   description: 'Youth cultural center offering art workshops, dance classes, theater, and creative spaces. Free activities for young people interested in arts and culture.',
  //   contact: {
  //     email: 'ungdom@kulturhuset.se',
  //     phone: '08-506 202 00'
  //   },
  //   website: 'https://kulturhuset.se/ungdom',
  //   discovery: {
  //     category: 'cultural',
  //     search_query: 'Stockholm kulturhus ungdom'
  //   },
  //   events: [
  //     {
  //       id: 'e10',
  //       organization_id: '5',
  //       name: 'Hip-Hop Dance Class',
  //       type: 'recurring',
  //       schedule: 'Mondays, 17:00-18:30',
  //       date: null,
  //       age_range: '13-19',
  //       description: 'Learn hip-hop dance from professional instructors. All levels welcome!'
  //     },
  //     {
  //       id: 'e11',
  //       organization_id: '5',
  //       name: 'Art Studio',
  //       type: 'recurring',
  //       schedule: 'Tuesdays and Fridays, 16:00-19:00',
  //       date: null,
  //       age_range: '13-25',
  //       description: 'Open art studio with materials provided. Paint, draw, or create freely.'
  //     },
  //     {
  //       id: 'e12',
  //       organization_id: '5',
  //       name: 'Youth Theater Performance',
  //       type: 'one-time',
  //       schedule: null,
  //       date: '2025-12-15',
  //       age_range: '15-25',
  //       description: 'Annual youth theater showcase featuring performances by young artists'
  //     }
  //   ]
  // }
];
