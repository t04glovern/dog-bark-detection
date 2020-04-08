<!--
    Dog Bark Detection App
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container>
        <v-data-table sort-by="timestamp"
                      sort-desc
                      :loading="loading"
                      :headers="headers"
                      :items="detections">

            <template v-slot:item.timestamp="{ item }">
                {{ item.timestamp.toLocaleString() }}
            </template>

            <template v-slot:item.certainty="{ item }">
                {{ (item.certainty * 100).toFixed(1) }}%
            </template>

            <template v-slot:item.audioUrl="{ item }">
                <div class="d-flex">
                    <template v-if="item.audioUrl === audioUrl">
                        <v-progress-linear color="primary"
                                           style="min-width: 120px"
                                           class="mr-2 align-self-center"
                                           :value="audioPosition / audioDuration * 100"
                                           :indeterminate="audioBuffering" />
                        <v-btn small icon
                               color="primary"
                               @click="onPlayStopAudio(item)">
                            <v-icon small>{{ audioPlaying ? "mdi-stop" : "mdi-play" }}</v-icon>
                        </v-btn>
                    </template>

                    <template v-else>
                        <v-progress-linear style="min-width: 120px"
                                           class="mr-2 align-self-center"
                                           :color="audioPlaying ? 'grey' : 'primary'" />

                        <v-btn small icon
                               color="primary"
                               :disabled="audioPlaying"
                               @click="onPlayStopAudio(item)">
                            <v-icon small>mdi-play</v-icon>
                        </v-btn>
                    </template>
                </div>
            </template>

            <template v-slot:item.actions="{ item }">
                <v-btn small icon
                       :color="item.rating === 'accurate' ? 'primary' : ''"
                       @click="onThumbUp(item)">
                    <v-icon small>mdi-thumb-up</v-icon>
                </v-btn>
                <v-btn small icon
                       :color="item.rating === 'inaccurate' ? 'primary' : ''"
                       @click="onThumbDown(item)">
                    <v-icon small>mdi-thumb-down</v-icon>
                </v-btn>
            </template>
        </v-data-table>
    </v-container>
</template>

<!--suppress JSUnusedGlobalSymbols -->
<script lang="ts">
    import {
        Component,
        Vue,
    } from "vue-property-decorator";

    import { getModule } from "vuex-module-decorators";

    import { AppModule } from "@/store/app";
    import { IDetection } from "@/store/models";

    const app = getModule(AppModule);

    @Component
    export default class HomeView extends Vue {
        loading = true;
        headers = [
            {
                text: "Camera",
                align: "start",
                sortable: true,
                value: "camera",
            },
            {
                text: "Recorded On",
                align: "start",
                sortable: true,
                value: "timestamp",
            },
            {
                text: "Certainty",
                align: "right",
                sortable: true,
                value: "certainty",
            },
            {
                text: "Audio",
                align: "center",
                sortable: false,
                value: "audioUrl",
            },
            {
                text: "Actions",
                value: "actions",
                sortable: false,
            },
        ];

        audio = new Audio();
        audioUrl = "";
        audioBuffering = false;
        audioPlaying = false;
        audioDuration = 0;
        audioPosition = 0;

        get detections() {
            return app.detections;
        }

        resetAudio(url: string) {
            const playbackListeners = {
                canplay: this.onAudioFinishBuffering,
                durationchange: this.onAudioUpdate,
                timeupdate: this.onAudioUpdate,
                play: this.onAudioUpdate,
                pause: this.onAudioUpdate,
            };

            this.audioUrl = url;
            this.audioBuffering = true;
            this.audioDuration = 0;
            this.audioPosition = 0;

            this.audio.pause();
            Object.entries(playbackListeners).forEach(([k, v]) => this.audio.removeEventListener(k, v));

            this.audio = new Audio(url);
            Object.entries(playbackListeners).forEach(([k, v]) => this.audio.addEventListener(k, v));
        }

        onAudioFinishBuffering() {
            this.audioBuffering = false;
        }

        onAudioUpdate() {
            this.audioDuration = this.audio.duration;
            this.audioPosition = this.audio.currentTime;
            this.audioPlaying = !this.audio.paused;
        }

        onPlayStopAudio(e: IDetection) {
            if(this.audioPlaying) {
                this.audio.pause();
                this.audio.currentTime = 0;
            } else {
                this.resetAudio(e.audioUrl);
                this.audio.play();
            }
        }

        onThumbUp(e: IDetection) {
            app.doUpdateDetectionRating({
                detectionId: e.id,
                rating: "accurate",
            });
        }

        onThumbDown(e: IDetection) {
            app.doUpdateDetectionRating({
                detectionId: e.id,
                rating: "inaccurate",
            });
        }

        mounted() {
            app.doFetchDetectionsAndCameras().finally(() => this.loading = false);
        }
    }
</script>
