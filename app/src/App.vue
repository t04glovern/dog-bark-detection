<!--
    Dog Bark Detection App
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<template>
    <v-app>
        <v-app-bar app dark
                   clipped-left
                   color="primary">

            <v-app-bar-nav-icon @click="drawer = !drawer" />

            <span v-if="!$vuetify.breakpoint.xs"
                  class="title ml-3 mr-5 text-uppercase">
                Bark<span class="font-weight-light">Detector</span>
            </span>
        </v-app-bar>

        <v-navigation-drawer app clipped
                             v-model="drawer">
            <v-layout column fill-height>
                <v-list nav dense>
                    <v-list-item link exact
                                 color="primary"
                                 :to="{ name: 'HomeView' }">
                        <v-list-item-icon>
                            <v-icon color="primary">mdi-map-marker</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>Detections</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item link exact
                                 color="primary"
                                 :to="{ name: 'CameraView' }">
                        <v-list-item-icon>
                            <v-icon color="primary">mdi-cctv</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>Cameras</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item link exact
                                 color="primary"
                                 :to="{ name: 'AboutView' }">
                        <v-list-item-icon>
                            <v-icon color="primary">mdi-information</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>What's This?</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>

                <v-spacer />

                <v-list nav dense>
                    <v-list-item>
                        <v-layout row justify-center>
                            <v-btn small text
                                   href="https://twitter.com/RicoBeti"
                                   target="_blank"
                                   class="text-none"
                                   color="primary">
                                @RicoBeti
                            </v-btn>
                            <v-btn small text
                                   href="https://twitter.com/nathangloverAUS"
                                   target="_blank"
                                   class="text-none"
                                   color="primary">
                                @nathangloverAUS
                            </v-btn>
                        </v-layout>
                    </v-list-item>
                </v-list>
            </v-layout>
        </v-navigation-drawer>

        <v-content>
            <router-view />
        </v-content>
    </v-app>
</template>

<script lang="ts">
    import {
        Component,
        Vue,
    } from "vue-property-decorator";

    @Component
    export default class App extends Vue {
        drawer = null;
    }
</script>
