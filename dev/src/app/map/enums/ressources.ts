
type ResourceCategory = Record<string, string>;
export const RESOURCE_CATEGORIES: Record<string, ResourceCategory> = {
    wood: {
      ash: '/assets/icons/ressources/ash.webp',
      braidwood: '/assets/icons/ressources/braidwood.webp',
      eastern_hemlock: '/assets/icons/ressources/eastern_hemlock.webp',
      oak: '/assets/icons/ressources/oak.webp',
      western_larch: '/assets/icons/ressources/western_larch.webp',
      weeping_willow: '/assets/icons/ressources/weeping_willow.webp',
    },
    stone: {
      basalt: '/assets/icons/ressources/basalt.webp',      
      gneiss: '/assets/icons/ressources/gneiss.webp',
      granite: '/assets/icons/ressources/granite.webp',
      wyrdstone: '/assets/icons/ressources/wyrdstone.webp',
      slate: '/assets/icons/ressources/slate.webp',      
      limestone: '/assets/icons/ressources/limestone.webp',
      quartz: '/assets/icons/ressources/quartz.webp',
    },
    plant: {
      blood_boiled_spiritbloom: '/assets/icons/ressources/blood_boiled_spiritbloom.webp',
      daffodil: '/assets/icons/ressources/daffodil.webp',
      flax: '/assets/icons/ressources/flax.webp',
      giant_bluebell: '/assets/icons/ressources/giant_bluebell.webp',
      gloomy_pross_petals: '/assets/icons/ressources/gloomy_pross_petals.webp',
      grave_lily: '/assets/icons/ressources/grave_lily.webp',
      moonbell: '/assets/icons/ressources/moonbell.webp',
      spiritbloom: '/assets/icons/ressources/spiritbloom.webp',
      snowdrop: '/assets/icons/ressources/snowdrop.webp',
    },
    metal: {
      copper: '/assets/icons/ressources/copper.webp',
      gold: '/assets/icons/ressources/gold.webp',  
      iron: '/assets/icons/ressources/iron.webp',  
      rividium: '/assets/icons/ressources/rividium.webp',
      silver: '/assets/icons/ressources/silver.webp',
      stellarium: '/assets/icons/ressources/stellarium.webp',
      tin: '/assets/icons/ressources/tin.webp',
      zinc: '/assets/icons/ressources/zinc.webp',
      Sapphire: '/assets/icons/ressources/sapphire.webp',      
    },
    gem: {
      diamond: '/assets/icons/ressources/diamond.webp',
      emerald: '/assets/icons/ressources/emerald.webp',
      halcyonite: '/assets/icons/ressources/halcyonite.webp',
      lumadon: '/assets/icons/ressources/lumadon.webp',
      night_opal: '/assets/icons/ressources/night_opal.webp',
      opal: '/assets/icons/ressources/opal.webp',
      ruby: '/assets/icons/ressources/ruby.webp',
      sapphire: '/assets/icons/ressources/sapphire.webp',
    }
  } as const;
  
  export type ResourceType = keyof typeof RESOURCE_CATEGORIES[keyof typeof RESOURCE_CATEGORIES];

  