<template>
  <div id="app">
    <div id="wrapper">
      <b-navbar toggleable="lg" type="dark" variant="dark" sticky>
        <b-navbar-brand to="/">Prolifix Manager</b-navbar-brand>
        <b-collapse id="nav-collapse" is-nav>
          <b-navbar-nav>
            <b-nav-item to="/" active-class>Home</b-nav-item>
            <b-nav-item-dropdown text="Orders" active-class>
              <b-dropdown-item to="/orders">Orders List</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item-dropdown text="Inventory" active-class>
                <b-dropdown-item to="/inventory">Inventory</b-dropdown-item>
                <b-dropdown-item to="/inventory/checkins">checkins</b-dropdown-item>
                <b-dropdown-item to="/inventory/checkouts">checkouts</b-dropdown-item>
              </b-nav-item-dropdown>
            <b-nav-item-dropdown text="Organizations" active-class>
              <b-dropdown-item to="/organizations">Organizations List</b-dropdown-item>
            </b-nav-item-dropdown>
            <b-nav-item to="/barcodereader" active-class>barcodereader</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
        <b-navbar-toggle class="ml-auto mr-2 border-0" target="nav-collapse">
          <template #default="{ expanded }">
            <b-icon v-if="expanded" icon="chevron-bar-up"></b-icon>
            <b-icon v-else icon="chevron-bar-down"></b-icon>
          </template>
        </b-navbar-toggle>
        <b-navbar-nav>
          <b-nav-item right>
            <b-button class="btn rounded-circle p-0 m-1" v-b-toggle.account-sidebar-right type="button" id="button-addon2">
              <AvatarIcon :user_data="userData" :logged_in_state="loggedInState"></AvatarIcon>
            </b-button>
          </b-nav-item>
        </b-navbar-nav>
      </b-navbar>
      <div>
        <b-sidebar id="account-sidebar-right" title="Account Options" :right="true" shadow :lazy="true" backdrop-variant="dark">
          <div class="px-3 py-2">
            <router-link v-if="!loggedInState" class="nav-link px-0" to="/login">
              Login
            </router-link>
            <div v-else class="nav-link px-0" v-on:click="logout">
              Logout
            </div>
          </div>
        </b-sidebar>
      </div>
      <div class="container-fluid">
        <div class="row justify-content-center">
          <!-- This is the link that vue uses to include other templates, Do not Delete! -->
          <router-view @login="updateUserData"/>
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

<script>

import AvatarIcon from './components/AvatarIcon.vue'

function getCookie (name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

export default {
  name: 'AppFrame',
  data: function () {
    return {
      userData: {},
      loggedInState: false
    }
  },
  methods: {
    logout: function () {
      const fetchRequest = window.origin + '/api/v1/auth/sessions'
      console.log(
        'DELETE ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          this.loggedInState = false
          this.userData = {
            department: '',
            doc: {},
            first_name: '',
            job_description: '',
            last_name: '',
            organization_id: 0,
            person_id: 0,
            profile_picture: '',
            user_id: '',
            username: ''
          }
          this.$router.push({ name: 'login' })
        } else {
          console.log(response)
        }
      }).catch(error => {
        console.log(error)
      })
    },
    updateUserData: function (userDataFromLogin) {
      console.log('Update Login Status: ', userDataFromLogin.data[0])
      this.userData = userDataFromLogin.data[0]
      this.loggedInState = true
    },
    getUser: function () {
      // Get session cookie data
      const sessionToken = getCookie('session')
      console.log('Saved Session Token: ', sessionToken)

      // Get user data
      const fetchRequest = window.origin + '/api/v1/auth/sessions?session-token=' + sessionToken
      console.log(
        'GET ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'GET',
        credentials: 'include'
      }).then(response => {
        if (response.status === 200) {
          response.json().then(jsonData => {
            this.userData = jsonData.data[0]
            console.log(this.userData)
            if (this.userData.user_id !== '') {
              this.loggedInState = true
            } else {
              this.loggedInState = false
            }
            const sessionToken = getCookie('session')
            console.log('Session Token: ', sessionToken)
          })
        } else {
          console.log('Looks like there was a problem. Status Code:' + response.status)
          response.json().then(jsonData => {
            console.log(jsonData)
            this.loggedInState = false
            const sessionToken = getCookie('session')
            console.log('New Session Token: ', sessionToken)
          })
        }
      })
    }
  },
  created: function () {
    this.getUser()
  },
  components: {
    AvatarIcon
  }
}
</script>

<style>
#wrapper {
  min-height: calc(100vh - 70px);
}

#footer {
  height: 56px;
}

.card {
  box-shadow: 0 20px 40px rgba(0,0,0,.2);
}
</style>
