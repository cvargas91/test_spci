<template>
  <div id="plotly_chart" />
</template>

<script>
import { newPlot } from "plotly.js";

import { defineComponent, onMounted } from "vue";

export default defineComponent({
  name: "Plotly",
  setup() {
    onMounted(async () => {
      await newPlot("plotly_chart", [
        {
          x: [1, 2, 3, 4],
          y: [3, 1, 4, 1],
        },
      ]);
    });
  },
});
</script>
