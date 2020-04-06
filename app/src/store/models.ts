/*
 * Dog Bark Detection App
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

export type DetectionRating = "accurate" | "inaccurate" | "unknown";

export interface ICamera {
    id: string;
    name: string;
    coordinates: [number, number];
    latestPhotoUrl?: string;
    latestPhotoDateTime?: Date;
}

export interface IDetection {
    id: string;
    camera: string;
    timestamp: Date;
    certainty: number;
    audioUrl: string;
    rating: DetectionRating;
}
