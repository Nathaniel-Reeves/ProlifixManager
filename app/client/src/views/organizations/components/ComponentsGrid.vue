<template>
    <Grid :cols="cols" :rows="rows" :pagination="{'limit':5}" :sort="true"></Grid>
</template>

<script>
import { h } from 'gridjs'
import Grid from 'gridjs-vue'

export default {
  name: 'ComponentsGrid',
  components: {
    Grid
  },
  props: {
    Components: Array
  },
  data () {
    return {
      cols: [
        {
          name: 'Component Name'
        },
        {
          name: 'Type'
        },
        {
          name: 'Actions',
          formatter: (cell, row) => {
            return h('button', {
              className: 'btn btn-secondary rounded-pill',
              onClick: () => this.view_row(cell, row)
            }, 'View')
          }
        }
      ],
      component_data: Object.values(this.Components),
      rows: [],
      pagination: {
        limit: 5
      }
    }
  },
  methods: {
    view_row: function (cell, row) {
      this.$router.push({ name: 'home' })
    }
  },
  created: function () {
    if (this.Components !== undefined) {
      this.component_data.forEach(component => {
        const row = [
          component.component_id,
          component.component_type,
          component.component_id
        ]
        this.rows.push(row)
      })
    }
  }
}
</script>
