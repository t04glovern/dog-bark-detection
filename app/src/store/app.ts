/*
 * Dog Bark Detection App
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";

import Amplify, { API, graphqlOperation } from "aws-amplify";
import { listBarks } from "@/graphql/queries";

const awsconfig = require("@/aws-exports").default;

Amplify.configure(awsconfig);

import {
    VuexModule,
    Module,
    Mutation,
    Action,
} from "vuex-module-decorators";

import store from "@/store";

import {
    DetectionRating,
    ICamera,
    IDetection,
} from "@/store/models";

@Module({
    store,
    dynamic: true,
    namespaced: true,
    name: "app",
})
export class AppModule extends VuexModule {
    cameras: ICamera[] = [];
    detections: IDetection[] = [];

    @Mutation
    setCameras(payload: { cameras: ICamera[] }) {
        this.cameras = payload.cameras;
    }

    @Mutation
    setDetections(payload: { detections: IDetection[] }) {
        this.detections = payload.detections;
    }

    @Mutation
    setDetectionRating(payload: { detectionId: string; rating: DetectionRating }) {
        const detection = this.detections.find(d => d.id === payload.detectionId);
        if(detection) {
            Vue.set(detection, "rating", payload.rating);
        }
    }

    @Action({rawError: true})
    async doFetchDetectionsAndCameras() {
        // TODO: Fetch from DynamoDB.
        const cameras: ICamera[] = [
            {
                id: "1",
                name: "Cam01",
                coordinates: [0, 0],
                latestPhotoUrl: "https://picsum.photos/seed/1/500/500",
                latestPhotoDateTime: new Date(),
            },
            {
                id: "2",
                name: "Cam02",
                coordinates: [0, 0],
                latestPhotoUrl: "https://picsum.photos/seed/2/500/500",
                latestPhotoDateTime: new Date(),
            },
            {
                id: "3",
                name: "Cam03",
                coordinates: [0, 0],
                latestPhotoUrl: "https://picsum.photos/seed/3/500/500",
                latestPhotoDateTime: new Date(),
            },
        ];

        const allBarks = await API.graphql(graphqlOperation(listBarks, {limit: 500}));
        const detections: IDetection[] = (allBarks as any)
            .data.listBarks.items.map((b: any): IDetection => ({
                id: b.deviceId,
                camera: b.camera,
                timestamp: new Date(b.timestamp * 1000),
                certainty: parseFloat(b.probability),
                audioUrl: b.wav_file,
                rating: "unknown", // TODO: Include rating in query.
            }));

        this.setCameras({cameras});
        this.setDetections({detections});
    }

    @Action({rawError: true})
    async doUpdateDetectionRating(payload: { detectionId: string; rating: DetectionRating }) {
        // TODO: Update detection rating in DynamoDB.
        this.setDetectionRating(payload);
    }
}
