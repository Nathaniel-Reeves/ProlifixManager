<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <router-link class="navbar-brand" to="/">Prolifix Manager</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavDropdown">
        <ul class="navbar-nav">
            <li class="nav-item active">
              <router-link class="nav-link" to="/">Home <span class="sr-only">(current)</span></router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/about">About</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/barchart">Bar Chart Test</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/bootstrap">Bootstrap Test</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/gridchart">Grid Chart Test</router-link>
            </li>
          <li class="nav-item dropdown">
            <router-link class="nav-link dropdown-toggle" to="/organizations" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              Organizations
            </router-link>
            <div class="dropdown-menu bg-dark" aria-labelledby="navbarDropdownMenuLink">
              <router-link class="nav-link" to="/organizations/clients">Clients</router-link>
            </div>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
      <div class="row justify-content-center">
        <!-- This is the link that vue uses to include other templates, Do not Delete! -->
        <router-view/>
      </div>
    </div>
  </div>
</template>
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

@import'~bootstrap/dist/css/bootstrap.css'
</style>
