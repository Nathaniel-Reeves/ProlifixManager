import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import(/* webpackChunkName: "barchart" */ '../views/HomeView.vue')
  },
  // {
  //   path: '/inventory',
  //   name: 'inventory',
  //   component: () => import(/* webpackChunkName: "inventory" */ '../views/inventory/InventoryHome.vue'),
  //   children: [
  //     {
  //       path: '/checkins',
  //       name: 'checkins',
  //       component: () => import(/* webpackChunkName: "checkins" */ '../views/inventory/InventoryHome.vue')
  //     },
  //     {
  //       path: '/checkouts',
  //       name: 'checkouts',
  //       component: () => import(/* webpackChunkName: "checkouts" */ '../views/inventory/InventoryHome.vue')
  //     }
  //   ]
  // },
  {
    path: '/catalogue',
    name: 'catalogue',
    children: [
      {
        path: 'components',
        name: 'components',
        props: route => ({ type: route.query.type }),
        component: () => import(/* webpackChunkName: "CatalogueHome" */ '../views/catalogue/components/ComponentHome.vue')
      },
      {
        path: 'components/create',
        props: route => ({ orgId: route.query.orgId, orgName: route.query.orgName, orgInitial: route.query.orgInitial }),
        name: 'NewComponent',
        component: () => import(/* webpackChunkName: "NewComponent" */ '../views/catalogue/components/NewComponent.vue')
      },
      {
        path: 'components/:id',
        name: 'ComponentDetail',
        component: () => import(/* webpackChunkName: "ComponentDetail" */ '../views/catalogue/components/ComponentDetail.vue')
      },
      {
        path: 'products',
        name: 'products',
        component: () => import(/* webpackChunkName: "ProductHome" */ '../views/catalogue/products/ProductHome.vue')
      },
      {
        path: 'products/:id',
        name: 'ProductDetail',
        component: () => import(/* webpackChunkName: "ProductDetail" */ '../views/catalogue/products/ProductDetail.vue')
      },
      {
        path: 'products/create',
        props: route => ({ orgId: route.query.orgId, orgName: route.query.orgName, orgInitial: route.query.orgInitial }),
        name: 'NewProduct',
        component: () => import(/* webpackChunkName: "NewProduct" */ '../views/catalogue/products/NewProduct.vue')
      }
    ]
  },
  {
    path: '/organizations',
    name: 'organizations',
    component: () => import(/* webpackChunkName: "organizations" */ '../views/organizations/OrganizationsHome.vue')
  },
  {
    path: '/organizations/create',
    name: 'NewOrganization',
    component: () => import(/* webpackChunkName: "NewOrganization" */ '../views/organizations/NewOrganization.vue')
  },
  {
    path: '/organizations/facilities/:id',
    name: 'FacilitiesDetail',
    component: () => import(/* webpackChunkName: "FacilitiesDetail" */ '../views/organizations/FacilitiesDetail.vue')
  },
  {
    path: '/organizations/facilities/create',
    props: route => ({ orgId: route.query.orgId, orgName: route.query.orgName, orgInitial: route.query.orgInitial }),
    name: 'NewFacility',
    component: () => import(/* webpackChunkName: "NewProduct" */ '../views/organizations/NewFacility.vue')
  },
  {
    path: '/organizations/people/:id',
    name: 'PeopleDetail',
    component: () => import(/* webpackChunkName: "PeopleDetail" */ '../views/organizations/PeopleDetail.vue')
  },
  {
    path: '/organizations/people/create',
    props: route => ({ orgId: route.query.orgId, orgName: route.query.orgName, orgInitial: route.query.orgInitial }),
    name: 'NewPerson',
    component: () => import(/* webpackChunkName: "NewProduct" */ '../views/organizations/NewPerson.vue')
  },
  {
    path: '/organizations/:id',
    name: 'OrganizationsDetail',
    component: () => import(/* webpackChunkName: "organizations" */ '../views/organizations/OrganizationDetail.vue')
  },
  {
    path: '/orders',
    name: 'orders',
    // component: () => import(/* webpackChunkName: "orders" */ '../views/orders/OrdersHome.vue'),
    children: [
      {
        path: 'po',
        name: 'PurchaseOrdersHome',
        component: () => import(/* webpackChunkName: "purchase_orders" */ '../views/orders/purchase_orders/PurchaseOrdersHome.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/LogIn.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import(/* webpackChunkName: "login" */ '../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
