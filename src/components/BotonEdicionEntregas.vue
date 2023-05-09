<template>
  <q-btn
    v-if="seRenderea"
    :label="etiqueta"
    color="info"
    @click="editaEntrega"
  />
</template>
<script>
import { ref, defineComponent } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { route } from "quasar/wrappers";

export default defineComponent({
  props: {
    usuario: Object,
    entrega: Object,
    tipoEntrega: String,
  },
  emits:['mantencion'],
  setup(props, {emit}) {
    const store = useStore();
    const router = useRouter();
    const seRenderea = ref(true);
    const user = props.entrega.usuario;
    const etiqueta = ref("");
    const tipoEntrega = props.tipoEntrega;
    const entrega = props.entrega;
    const accion = ref("");
    //VARIABLE "mantencionPOA2023" implica control a actualizaciones relacionadas al nuevo modelo y sábana de datos
    const mantencionPOA2023 = ref(false);

    if (
      (props.entrega.estado == "Borrador" ||
        props.entrega.estado == "Rechazado por líder" ||
        props.entrega.estado == "Rechazado por UPCI") &&
      props.usuario.id == props.entrega.usuario.id
    ) {
      etiqueta.value = " Editar Entrega ";
      if (props.entrega) accion.value = "colabEdita";
    } else seRenderea.value = false;
    
    return {
      mantencionPOA2023,
      etiqueta,
      seRenderea,
      entrega,
      tipoEntrega,
      editaEntrega: () => {
        store.dispatch("entrega/setEntregaAModificar", {
          entrega: props.entrega,
        });
        if (tipoEntrega === "verificador") router.push("editaVerificador");
        else router.push("editaProducto");
      },
    };
  },
});
</script>
