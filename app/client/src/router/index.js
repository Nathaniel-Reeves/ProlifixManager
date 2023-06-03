import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/barchart',
    name: 'barchart',
    component: () => import(/* webpackChunkName: "barchart" */ '../views/BarChart.vue')
  },
  {
    path: '/bootstrap',
    name: 'bootstrap',
    component: () => import(/* webpackChunkName: "bootstrap" */ '../views/BootstrapFour.vue')
  },
  {
    path: '/gridchart',
    name: 'gridchart',
    component: () => import(/* webpackChunkName: "gridchart" */ '../views/GridChart.vue')
  },
  {
    path: '/organizations',
    name: 'organizations',
    component: () => import(/* webpackChunkName: "organizations" */ '../views/organizations/OrganizationsHome.vue'),
    children: [
      {
        path: 'clients',
        name: 'clients',
        component: () => import(/* webpackChunkName: "clients" */ '../views/organizations/ClientsOrg.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

export default router
