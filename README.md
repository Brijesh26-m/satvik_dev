# Satvik Roots — Luxury Pure Vegetarian Dining

A cinematic, luxury digital web experience for **Satvik Roots**, celebrating pure vegetarian culinary heritage with modern, interactive aesthetics.

[![Vercel Deployment](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=flat&logo=vercel)](https://satvikdev-d3jd.vercel.app)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.7-blue?logo=typescript)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-18.3-61dafb?logo=react)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38b2ac?logo=tailwind-css)](https://tailwindcss.com/)
[![GSAP](https://img.shields.io/badge/GSAP-3.15-88CE02?logo=greensock)](https://greensock.com/gsap/)

---

## 🌟 Highlights & Features

- **Cinematic Dark-Gold Aesthetic**: Deep obsidian & marble surfaces with warm golden accents, bespoke typography, and subtle ambient lighting.
- **Interactive 3D Luxury Menu Book**: Flip-through physical book styling with realistic page turns, category browsing, and dish inspection.
- **Micro-Interactions & Magnetic Hover**: Liquid fills, magnetic physics on interactive buttons, and smooth GSAP-driven scroll transitions.
- **Verified Ordering Platforms**: Integrated order routing to verified delivery channels (Zomato, Swiggy, MagicPin, District Dining).
- **Cart & Reservation Drawer**: Direct table reservations, special request handling, and interactive item checkout.
- **Fully Responsive**: Flawlessly engineered across ultra-wide desktop (1440p+), laptop (1280px), tablet (768px), and mobile viewports.

---

## 🛠️ Tech Stack

- **Framework**: [React 18](https://react.dev/) + [Vite 6](https://vitejs.dev/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Animations**: [GSAP (GreenSock)](https://greensock.com/gsap/) + Custom CSS keyframes
- **Icons**: [Lucide React](https://lucide.dev/)
- **Hosting**: [Vercel](https://vercel.com/)

---

## 🚀 Getting Started

### Prerequisites

- Node.js `>= 18.0.0`
- npm `>= 9.0.0`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Brijesh26-m/satvik-roots-restaurant.git
   cd satvik-roots-restaurant
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run development server:
   ```bash
   npm run dev
   ```

4. Build for production:
   ```bash
   npm run build
   ```

5. Preview the production build locally:
   ```bash
   npm run preview
   ```

---

## 📂 Project Structure

```
satvik-roots-restaurant/
├── public/               # Static assets (images, audio/video, emblems, textures)
│   └── assets/
│       └── dishes/       # Dish imagery
├── src/
│   ├── components/       # UI components (Hero, Menu, Story, Reservation, etc.)
│   ├── config/           # Platform integrations & partner links
│   ├── context/          # React contexts (Cart, UI state)
│   ├── data/             # Dishes catalog, menu categories, restaurant config
│   ├── hooks/            # Custom React hooks (scroll, magnetic, media queries)
│   ├── styles/           # Global styles and custom CSS animations
│   ├── utils/            # Helper utilities
│   ├── App.tsx           # Main application view
│   └── main.tsx          # React application entry point
├── docs/                 # Documentation and integration guides
├── scripts/              # Data curation and asset automation scripts
├── vercel.json           # Vercel deployment configuration
└── vite.config.ts        # Vite configuration
```

---

## 🌐 Live Website

- **Production URL**: [https://satvikdev-d3jd.vercel.app](https://satvikdev-d3jd.vercel.app)
