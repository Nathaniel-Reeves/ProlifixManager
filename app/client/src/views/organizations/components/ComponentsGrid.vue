<template>
    <Grid :cols="cols" :rows="rows" :pagination="{'limit':5}" :sort="true"></Grid>
</template>

<script>
import Grid from 'gridjs-vue'

export default {
  name: 'ComponentsGrid',
  components: {
    Grid
  },
  props: {
    components: Object
  },
  data () {
    return {
      cols: ['Component Name', 'Type'],
      component_data: Object.values(this.components),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  created: function () {
    this.component_data.forEach(component => {
      const row = [
        component.component_name,
        component.component_type
      ]
      this.rows.push(row)
    })
  }
}
</script>
