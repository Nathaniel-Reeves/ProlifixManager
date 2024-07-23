<template>
  <b-card
    img-src="../assets/Company Images/logos jpg/Cropped Logo.jpg"
    img-alt="Prolifix Nutrition Logo"
    img-top
    style="max-width: 25rem;"
    class="p-4 mt-2 mb-4"
  >
    <b-card-text>
      <div class="hello">
        <StreamBarcodeReader
          @decode="(a, b, c) => onDecode(a, b, c)"
          @loaded="() => onLoaded()"
        ></StreamBarcodeReader>
        Input Value: {{ text || "Nothing" }}
      </div>
    </b-card-text>
    <b-card-text>
      <qr-code :text="text"></qr-code>
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
import { StreamBarcodeReader } from 'vue-barcode-reader'

export default {
  name: 'BarcodeReader',
  components: {
    StreamBarcodeReader
  },
  data () {
    return {
      text: '',
      id: null
    }
  },
  props: {
    msg: String
  },
  methods: {
    onDecode (a, b, c) {
      this.text = a
      if (this.id) clearTimeout(this.id)
      this.id = setTimeout(() => {
        if (this.text === a) {
          this.text = ''
        }
      }, 5000)
    },
    onLoaded () {
      // eslint-disable-next-line
      console.log('load')
    }
  }
}
</script>
