<!--
    Dog Bark Detection App
    Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
-->

<!--suppress HtmlUnknownTarget -->
<template>
    <v-container style="max-width: 1000px">
        <v-card class="mx-2">
            <div class="pt-4 title text-center">
                Barks / Day
            </div>
            <v-card-text>
                <canvas ref="chart" />
            </v-card-text>
        </v-card>
    </v-container>
</template>

<!--suppress JSUnusedGlobalSymbols -->
<script lang="ts">
    import {
        Component,
        Vue,
        Watch,
    } from "vue-property-decorator";

    import { Chart } from "chart.js";

    import { getModule } from "vuex-module-decorators";
    import { AppModule } from "@/store/app";

    const app = getModule(AppModule);

    @Component
    export default class DashboardView extends Vue {
        chart: Chart | null = null;

        get detections() {
            return app.detections;
        }

        // TODO: Ensure correctness and find better solution.
        get weekDayBarks() {
            const today = new Date();
            today.setHours(0, 0, 0, 0);

            const oneWeekAgo = today.getTime() - (60 * 60 * 24 * 7 * 1000);
            const aggregated = [0, 0, 0, 0, 0, 0, 0];

            app.detections
                .filter(d => d.timestamp.getTime() > oneWeekAgo)
                .forEach(d => {
                    aggregated[d.timestamp.getDay()] += 1;
                });

            const shifted = [0, 0, 0, 0, 0, 0, 0];
            aggregated.forEach((d, i) => shifted[(i + today.getDay()) % 7] = d);

            return aggregated;
        }

        get weekDayNames() {
            const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
            const today = new Date().getDay();
            const days = [];

            for(let i = 0; i < 7; i++) {
                let day = today - i;
                if(day < 0) {
                    day = 7 + day;
                }
                days.push(weekdays[day]);
            }

            return days.reverse();
        }

        @Watch("detections")
        onUpdateDetections() {
            if(this?.chart?.data?.datasets) {
                this.chart.data.datasets[0].data = this.weekDayBarks;
                this.chart.update();
            }
        }

        mounted() {
            if(app.detections.length === 0) {
                app.doFetchDetectionsAndCameras();
            }

            const context = (this.$refs.chart as HTMLCanvasElement).getContext("2d") as CanvasRenderingContext2D;
            this.chart = new Chart(context, {
                type: "bar",
                data: {
                    labels: this.weekDayNames,
                    datasets: [{
                        label: "Barks",
                        data: this.weekDayBarks,
                        yAxisID: "detections",
                        backgroundColor: "#e1bee7",
                    }],
                },
                options: {
                    responsive: true,
                    tooltips: {
                        mode: "index",
                        intersect: true,
                    },
                    scales: {
                        yAxes: [{
                            type: "linear",
                            display: true,
                            position: "left",
                            id: "detections",
                            gridLines: {
                                drawOnChartArea: false,
                            },
                        }],
                    },
                },
            });
        }

        destroyed() {
            if(this.chart) {
                this.chart.destroy();
                this.chart = null;
            }
        }
    }
</script>

<style lang="scss">

</style>
