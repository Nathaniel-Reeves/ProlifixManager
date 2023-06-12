<template>
  <div id="app">
    <div id="wrapper">
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <router-link class="navbar-brand" to="/">Prolifix Manager</router-link>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
          <ul class="navbar-nav">
            <li class="nav-item active">
              <router-link class="nav-link" to="/">Home<span class="sr-only">(current)</span></router-link>
            </li>
            <li class="nav-item dropdown">
                <router-link class="nav-link dropdown-toggle" to="/orders" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  Orders
                </router-link>
                <div class="dropdown-menu bg-dark" aria-labelledby="navbarDropdownMenuLink">
                  <router-link class="nav-link" to="/orders/lot_numbers">Lot Numbers</router-link>
                  <router-link class="nav-link" to="/orders/purchase_orders">Purchase Orders</router-link>
                  <router-link class="nav-link" to="/orders/sales_orders">Sales Orders</router-link>
                </div>
              </li>
            <li class="nav-item dropdown">
              <router-link class="nav-link dropdown-toggle" to="/organizations" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                Organizations
              </router-link>
              <div class="dropdown-menu bg-dark" aria-labelledby="navbarDropdownMenuLink">
                <router-link class="nav-link" to="/organizations/clients">Clients</router-link>
                <router-link class="nav-link" to="/organizations/suppliers">Suppliers</router-link>
                <router-link class="nav-link" to="/organizations/labs">Labs</router-link>
              </div>
            </li>
          </ul>
        </div>
      </nav>
      <div class="container-fluid">
        <div class="row justify-content-center">
          <!-- This is the link that vue uses to include other templates, Do not Delete! -->
          <router-view/>
        </div>
      </div>
    </div>
    <div class="container-fluid mt-3 p-0" id="footer">
      <footer class="bg-dark text-center text-white">
        <!-- <div class="container p-4 pb-0">
        <section class="">
          <form action="">
            <div class="row d-flex justify-content-center">
              <div class="col-auto">
                <p class="pt-2">
                  <strong>Sign up for our newsletter</strong>
                </p>
              </div>
              <div class="col-md-5 col-12">
                <div class="form-outline form-white mb-4">
                  <input type="email" id="form5Example2" class="form-control" />
                  <label class="form-label" for="form5Example2">Email address</label>
                </div>
              </div>
              <div class="col-auto">
                <button type="submit" class="btn btn-outline-light mb-4">
                  Subscribe
                </button>
              </div>
            </div>
          </form>
        </section>
      </div> -->
        <div class="text-center bg-dark p-3">
          © 2023 Copyright  |  v0.0.1-beta
        </div>
      </footer>
    </div>
  </div>
</template>
<style>
#wrapper {
  min-height: calc(100vh - 70px);
}

#footer {
  height: 56px;
}
</style>
