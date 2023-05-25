<template>
    <div class="barchart">
        <h1>This is a Chart Page</h1>
        <BarChart/>
    </div>
</template>
<script>
import BarChart from '../components/BarChart.vue'

export default {
  name: 'FirstBarChart',
  components: { BarChart }
}
</script>
