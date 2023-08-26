<template>
    <Grid :cols="cols" :rows="rows"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'CarsChart',
  components: {
    Grid
  },
  data () {
    return {
      cols: ['Make', 'Model', 'Year', 'Color'],
      rows: [
        ['Ford', 'Fusion', '2011', 'Silver'],
        ['Chevrolet', 'Cruz', '2018', 'White']
      ]
    }
  }
}
</script>
