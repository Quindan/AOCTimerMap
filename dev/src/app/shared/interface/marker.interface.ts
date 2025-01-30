// Interface pour les markers
export interface CustomMarker {
    id?: number;
    label: string;
    lat: number;
    lng: number;
    startTime: number;
    alarmAfter: number;
    inGameCoord: string;
    type: string;
    rarity: string;
    missing: boolean;
}

export interface MarkerForm {
    label: string,
    coord: string,
    type: string, 
    rarity: string, 
    updateTimer: boolean,
    timer: number  
}