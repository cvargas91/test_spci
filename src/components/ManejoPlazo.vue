<template>
    <q-item-section v-if="hito.plazo[0] && hito.plazo[0].anio > 2000">
        <b style="padding-top:5pt;padding-bottom:3pt;">Plazo:</b>
            {{ hito.plazo[0].mes}} - {{hito.plazo[0].anio }}
    </q-item-section>
    <q-item-section v-else-if="hito.plazo[0] && hito.plazo[0].anio < 2000">
        <b style="padding-top:5pt;padding-bottom:3pt;">Plazo:</b>
            {{ hito.plazo[0].mes}} - {{"20" + hito.plazo[0].anio }}
    </q-item-section>
    <q-item-section v-else>
        <b style="padding-top:5pt;padding-bottom:3pt;">Plazo:</b> 
            No definido
    </q-item-section>
</template>

<script>
import { ref, toRef, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

export default defineComponent({
    props: {
        hito: Object,
    },
    setup(props) {
        const router = useRouter();
        const store = useStore();
        return {
            hito: toRef(props, "hito"),
        };
    }
})
</script>