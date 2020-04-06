<!--
    Dog Bark Detection App
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container>
        <v-layout wrap>
            <v-flex v-for="cam in cameras"
                    :key="cam.id"
                    class="align-center justify-center"
                    xs12 mb-2 mb-sm-4>
                <v-card class="align-center justify-center align-self-center">
                    <div class="d-flex flex-no-wrap">
                        <v-avatar tile
                                  size="200"
                                  class="ma-2 ma-sm-4">
                            <v-img v-if="cam.latestPhotoUrl" :src="cam.latestPhotoUrl"></v-img>
                            <v-icon v-else x-large>mdi-image-off</v-icon>
                        </v-avatar>
                        <div>
                            <v-card-title class="headline">
                                {{ cam.name }}
                            </v-card-title>
                            <v-card-subtitle v-if="cam.latestPhotoDateTime" class="pb-1 caption">
                                <div>
                                    <v-icon x-small>mdi-calendar-clock</v-icon>
                                    {{ cam.latestPhotoDateTime.toLocaleString() }}
                                </div>

                                <div class="mr-2">
                                    <v-icon x-small>mdi-map-marker-radius</v-icon>
                                    {{ cam.coordinates[0].toFixed(6) }},
                                    {{ cam.coordinates[1].toFixed(6) }}
                                </div>
                            </v-card-subtitle>
                        </div>
                    </div>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script lang="ts">
    import {
        Component,
        Vue,
    } from "vue-property-decorator";

    import { getModule } from "vuex-module-decorators";

    import { AppModule } from "@/store/app";

    const app = getModule(AppModule);

    @Component
    export default class CameraView extends Vue {
        get cameras() {
            return app.cameras;
        }
    }
</script>
