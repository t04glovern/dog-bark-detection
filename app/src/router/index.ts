/*
 * Dog Bark Detection App
 * Copyright (c) 2020 by SilentByte <https://www.silentbyte.com/>
 */

import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "@/views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
    {
        path: "/",
        name: "HomeView",
        component: HomeView,
    },
    {
        path: "/dashboard",
        name: "DashboardView",
        component: () => import(/* webpackChunkName: "dashboard" */ "@/views/DashboardView.vue"),
    },
    {
        path: "/cameras",
        name: "CameraView",
        component: () => import(/* webpackChunkName: "cameras" */ "@/views/CameraView.vue"),
    },
    {
        path: "/about",
        name: "AboutView",
        component: () => import(/* webpackChunkName: "about" */ "@/views/AboutView.vue"),
    },
];

// noinspection TypeScriptUnresolvedVariable
const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});

export default router;
