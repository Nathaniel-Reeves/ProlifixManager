<template>
  <b-card
    img-src="../assets/Company Images/logos jpg/Cropped Logo.jpg"
    img-alt="Prolifix Nutrition Logo"
    img-top
    style="max-width: 25rem;"
    class="p-4 mt-2 mb-4"
  >
    <b-card-text>
        <b-form @submit.stop.prevent>
            <b-form-group>
                <label for="text-username">Username</label>
                <b-form-input type="text" v-model="username" id="text-username" aria-describedby="username-help-block"></b-form-input>
                <b-form-text id="username-help-block">
                </b-form-text>
            </b-form-group>
            <b-form-group>
                <label for="text-password">Password</label>
                <b-form-input type="password" v-model="password" id="text-password" aria-describedby="password-help-block"></b-form-input>
                <b-form-text id="password-help-block">
                </b-form-text>
            </b-form-group>
            <b-form-group>
                <b-button href="#" v-on:click="login()" class="d-flex justify-content-center" variant="primary">Login</b-button>
            </b-form-group>
        </b-form>
    </b-card-text>
    <!-- Show Flash Messages -->
    <div v-for="flash in flash_errors" v-bind:key="flash.error">
        <div class="alert alert-danger" role="alert">
            <p>{{ flash }}</p>
        </div>
    </div>
  </b-card>
</template>

<script>
export default {
  name: 'LogIn',
  data: function () {
    return {
      username: '',
      password: '',
      flash_errors: []
    }
  },
  methods: {
    login: function () {
      const fetchRequest = window.origin + '/api/auth/sessions'

      console.log(
        'POST ' + fetchRequest
      )
      fetch(fetchRequest, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      }).then(response => {
        if (response.status === 200) {
          response.json().then(data => {
            console.log(data)
            this.flash_errors.push(data.error)
          })
        } else {
          console.log(response)
          this.flash_errors.push(response.json().error)
          console.log(this.flash_errors)
        }
      }).catch(error => {
        console.log(error)
        this.flash_errors.push(error)
        console.log(this.flash_errors)
      })
    }
  }
}
</script>
