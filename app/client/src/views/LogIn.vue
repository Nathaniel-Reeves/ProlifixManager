<template>
  <b-card
    img-src="../assets/Company Images/logos jpg/Cropped Logo.jpg"
    img-alt="Prolifix Nutrition Logo"
    img-top
    style="max-width: 25rem;"
    class="p-4 mt-2 mb-4"
  >
    <b-card-text>
        <!-- Show Flash Messages -->
        <div v-for="flash in flash_errors" v-bind:key="flash.error">
          <div class="alert alert-danger" role="alert">
            <p>{{ flash.message_detail }}</p>
          </div>
        </div>
        <b-form @submit.stop.prevent>
            <b-form-group>
                <label for="text-username">Username</label>
                <b-form-input type="text" class="form-control" v-model="username" id="text-username"></b-form-input>
                <b-form-text>
                  {{ usernameMessages.message }}
                </b-form-text>
            </b-form-group>
            <b-form-group>
                <label for="text-password">Password</label>
                <b-form-input type="password" class="form-control" v-model="password" id="text-password"></b-form-input>
                <b-form-text>
                  {{ passwordMessages.message }}
                </b-form-text>
            </b-form-group>
            <b-form-group>
                <b-button href="#" v-on:click="login()" class="d-flex justify-content-center" variant="primary">Login</b-button>
            </b-form-group>
        </b-form>
    </b-card-text>
  </b-card>
</template>

<script>
export default {
  name: 'LogIn',
  data: function () {
    return {
      username: '',
      password: '',
      form_messages: {},
      flash_messages: [],
      userData: {}
    }
  },
  methods: {
    login: function () {
      const fetchRequest = window.origin + '/api/v1/auth/sessions'
      // eslint-disable-next-line
      console.log(
        'POST ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      }).then(response => {
        response.json().then(jsonData => {
          if (response.status === 201) {
            this.userData = jsonData
            this.$emit('login', jsonData)
            this.$router.push({ name: 'home' })
          } else if (response.status === 401) {
            this.form_messages = jsonData.messages.form
          } else {
            response.json().then(data => {
              this.flash_messages = data.messages.flash
              const createToast = this.$parent.createToast
              this.flash_messages.forEach(function (message) {
                createToast(message)
              })
            })
          }
        })
      }).catch(error => {
        // eslint-disable-next-line
        console.log(error)
        this.flash_errors.push(error)
        // eslint-disable-next-line
        console.log(this.flash_errors)
      })
    }
  },
  computed: {
    usernameMessages: function () {
      if (this.form_messages.username === undefined) {
        return {
          message: ''
        }
      } else {
        return this.form_messages.username
      }
    },
    passwordMessages: function () {
      if (this.form_messages.password === undefined) {
        return {
          message: ''
        }
      } else {
        return this.form_messages.password
      }
    }
  }
}
</script>
