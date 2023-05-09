<template>
  <div v-if="entrega.estadoWorkflow" class="q-pa-md">
    <q-card class="my-card bg-teal-2">
      <q-card-section horizontal>
          <q-card-section>
              <q-avatar color="white" text-color="cyan-8" icon="done" />
          </q-card-section>
          <q-card-section class="text-textoAzul">
              <div class="text-h6"><b>Estado de la entrega actualizado.</b></div>
              Gracias por usar Colabora
          </q-card-section>
      </q-card-section>      
      <q-card-section class="q-pt-none">
          <q-btn color="light-blue-10"
              label="Volver a la bandeja de entregas"
              @click="limpiaBandeja"
          />
      </q-card-section>
      <q-card-section>
          <q-separator class="bg-textoAzul" inset />
      </q-card-section>
    </q-card>

  </div>
  <div v-else class="q-pa-md">
    <div class="text-h6">
      Rechazando {{ entrega.aRechazar.tipoEntrega }}
      <i>{{ entrega.aRechazar.entrega.descripcion }}</i>
    </div>
    <q-form @submit="onSubmit" class="q-gutter-md">
      <q-input
        filled
        v-model="txtRetroalimentacion"
        label="Retroalimentación de la entrega rechazada"
        hint="Dar indicaciones que permitan a su colaborador o colaboradora volver a subir una entrega que cumpla lo exigido"
        lazy-rules
        type="textarea"
        :rules="[
          (val) =>
            (val && val.length > 10) || 'Escriba por lo menos 10 caracteres',
        ]"
      />
      <div>
        <q-btn label="Enviar" type="submit" color="primary" />
      </div>
    </q-form>
  </div>
</template>
<script>
import { computed, ref } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const store = useStore();
    const entrega = computed(() => store.state.entrega);
    const txtRetroalimentacion = ref(null);
    return {
      txtRetroalimentacion,
      entrega,
      limpiaBandeja: () => {
        let rutaDestino =
          entrega.value.aRechazar.mandante == "UPCI"
            ? "bandejaUPCI"
            : "bandejaEntregas";
        store.dispatch("entrega/limpiaEntregas");
        router.push(rutaDestino);
      },
      onSubmit: () => {
        if (confirm("¿Enviar retroalimentación?")) {
          if (entrega.value.aRechazar.mandante == "lider")
            store.dispatch("entrega/workflowLiderRechaza", {
              entrega_id: entrega.value.aRechazar.entrega.id,
              entrega_tipo: entrega.value.aRechazar.tipoEntrega,
              retroalimentacion: txtRetroalimentacion.value,
            });
          else if (entrega.value.aRechazar.mandante == "UPCI")
            store.dispatch("entrega/workflowUPCIRechaza", {
              entrega_id: entrega.value.aRechazar.entrega.id,
              entrega_tipo: entrega.value.aRechazar.tipoEntrega,
              retroalimentacion: txtRetroalimentacion.value,
            });
          else {
          }
        }
      },
    };
  },
};
</script>

