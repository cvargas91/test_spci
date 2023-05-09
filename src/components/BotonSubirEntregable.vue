<template>
  <div class="text-h6 q-mb-md" v-if="seRenderea">
    Acción <b> Sin {{ tipoTactica }} </b> {{ asociado }}.
  </div>  
  <q-btn
    :label="etiqueta"
    class="q-ma-sm"
    color="secondary"
    no-caps
    @click="subirEntrega"
  />
</template>
<script>
import { ref, toRef, defineComponent, computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { useQuasar } from "quasar";

export default {
  props: {
    tipoEntrega: String,
    tipoTactica: String,
    referencia: String,
  },
  watch:{
    referencia: function(newValue){
      this.subirEntrega();
    }
  },
  emits:['mantencion'],
  setup(props, {emit}) {
    const $q = useQuasar();
    const store = useStore();
    const router = useRouter();
    const seRenderea = ref(false);
    const tipoEntrega = props.tipoEntrega;
    const tipoTactica =
      props.tipoTactica[0].toUpperCase() + props.tipoTactica.slice(1);
    const referencia = toRef(props, "referencia");
    const etiqueta = ref("Subir " + tipoEntrega);
    const asociado = ref("");
    //VARIABLE "mantencionPOA2023" implica control a actualizaciones relacionadas al nuevo modelo y sábana de datos
    const mantencionPOA2023 = ref(false);
    const subirEntrega = () => {      
      store.dispatch("accion/referenciaSubirEntregable", referencia.value);
      const detalleAccion = store.state.accion.detalleAccion;
      if (tipoEntrega === "verificador") {
        if (!detalleAccion.funciones.length) {
          seRenderea.value = true;
          asociado.value = "asociadas";
        } else {
          router.push("subirVerificador");
        }
      } else {
        if (!detalleAccion.hitos.length) {
          seRenderea.value = true;
          asociado.value = "asociados";
        } else {
          router.push("subirProducto");
        }
      }
    };

    return {
      etiqueta,
      seRenderea,
      subirEntrega: subirEntrega,
      tipoTactica,
      asociado,
      mantencionPOA2023
    };
  },
};
</script>
