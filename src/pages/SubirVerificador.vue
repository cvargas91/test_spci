<template>
  <div class="q-pa-md">
    <PopupCancelarNuevaEntrega
      :mostrar="mostrarPopupCancelar"
      @update:mostrar="mostrarPopupCancelar = $event"
      @respuestaPopup="handlerPopupCancelar"
    />
    <div v-if="entrega.estadoWorkflow == 'EnviadoAlLider'">
      <div class="text-h6">¡Felicitaciones!</div>
      <p>Se ha enviado el nuevo borrador al líder del equipo</p>
      <q-btn
        label="OK. Ir a la bandeja de entregas"
        class="q-ma-sm"
        to="bandejaEntregas"
        color="primary"
      />
    </div>
    <div v-else-if="verificador.nuevoVerificador">
      <div class="text-h6 text-textoAzul">¡Felicitaciones!</div>
      <p>Se ha guardado el nuevo verificador como borrador</p>
      <div class="text-h6 text-textoAzul">
        ¿Está listo tu nuevo verificador para ser revisado por el líder del
        equipo?
      </div>
      <div>
        <q-btn
          label="No no no, déjalo como borrador. Lo enviaré más tarde"
          class="q-ma-sm"
          to="bandejaEntregas"
          color="primary"
        />
        <q-btn
          class="q-ma-sm"
          label="Sí, envíalo al líder"
          @click="enviaAlLider"
          color="secondary"
        />
      </div>
    </div>
    <div v-else-if="entrega.nuevaEntrega">
      <q-stepper
        v-model="step"
        ref="stepper"
        color="blue"
        animated
        header-class="tablaAcciones"
      >
        <q-step
          :name="1"
          title="Indicador"
          icon="settings"
          :done="step > 1"
          class="tarjetaAmarilla"
        >
          <div class="text-h6">
            Seleccione un verificador de las siguientes funciones de
            {{ entrega.nuevaEntrega.id_uaysen }}
          </div>
          <div class="text-subtitle1">
            {{ entrega.nuevaEntrega.titulo }}
          </div>
          <div class="text-subtitle2">
            Objetivo: {{ entrega.nuevaEntrega.objetivo }}
          </div>
          <div class="row" v-for="item in accion.funciones" :key="item.id">
            <div class="col">
              <q-card class="tarjetaAmarilla">
                <q-card-section class="q-pa-sm">
                  <div class="text-body1">{{ item.nombre }}</div>
                </q-card-section>
                <q-card-actions vertical>
                  <div v-if="item.indicador_set.length" class="column">
                    <q-btn-toggle
                      no-caps
                      align="left"
                      class="col"
                      v-for="subItem in item.indicador_set"
                      :key="subItem.id"
                      v-model="indicadorSeleccionado"
                      toggle-color="primary"
                      :options="[{ label: subItem.nombre, value: subItem }]"
                    />
                  </div>
                  <div v-else="item.indicador_set.length" class="bg-accent">
                    No hay indicadores definidos para esta función. Por favor,
                    notificar este incidente a UPCI para ser revisado. Gracias
                  </div>
                </q-card-actions>
              </q-card>
            </div>
          </div>
        </q-step>
        <q-step
          :name="2"
          title="Detalles"
          icon="assignment"
          :done="step > 2"
          class="tarjetaAmarilla"
        >
          <div class="row">
            <div class="col q-ma-sm">
              <q-card flat class="tarjetaAmarilla">
                <q-card-section>
                  <div class="text-h6">
                    {{ indicadorSeleccionado.nombre }}
                  </div>
                </q-card-section>
                <q-separator inset />
                <q-card-section class="q-pt-none">
                  <div class="text-weight-bold">Fórmula</div>
                  {{ indicadorSeleccionado.formula }}
                </q-card-section>
                <q-card-section class="q-pt-none">
                  <div class="text-weight-bold">Meta</div>
                  {{ indicadorSeleccionado.meta }}
                </q-card-section>
                <q-card-section class="q-pt-none">
                  <div class="text-weight-bold">Verificador</div>
                  {{ indicadorSeleccionado.nombreVerificador }}
                </q-card-section>
              </q-card>
            </div>
            <div class="col q-ma-sm">
              <q-card flat class="tarjetaAmarilla">
                <q-card-section>
                  <div class="text-h6">Indique el avance del indicador</div>
                </q-card-section>
                <q-separator inset />
                <q-form class="q-gutter-md">
                  <q-card-section class="q-pt-none">
                    <q-input
                      filled
                      v-model="verificadorValor"
                      :label="indicadorSeleccionado.formula"
                      hint="Valor del indicador al día de hoy"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) || 'Debe ingresar un valor',
                      ]"
                    />
                  </q-card-section>
                  <q-card-section class="q-pt-none">
                    <q-input
                      type="textarea"
                      filled
                      v-model="verificadorDescripcion"
                      label="Descripción o comentarios sobre valor indicado"
                      lazy-rules
                      :rules="[
                        (val) =>
                          (val && val.length > 0) ||
                          'Debe ingresar una descripción o comentario',
                      ]"
                    />
                  </q-card-section>
                </q-form>
              </q-card>
            </div>
          </div>
          <q-separator inset />
        </q-step>
        <q-step
          :name="3"
          title="Adjunta"
          icon="create_new_folder"
          class="tarjetaAmarilla"
        >
          <div class="text-h6">Adjuntar el verificador</div>
          <p>
            Adjunta documentos que necesites para demostrar el avance del
            indicador. Éstos quedarán almacenados en Google Drive y serán
            revisados por tu jefatura y el equipo de UPCI
          </p>
          <Picker :baseDir="indicadorSeleccionado.dirGoogle" />
          <div
            v-if="entrega.adjuntosNuevaEntrega"
            class="q-pa-md"
            style="max-width: 400px"
          >
            <div class="text-weight-bold">
              Documentos subidos a Google Drive:
            </div>
            <q-list
              bordered
              v-for="item in entrega.adjuntosNuevaEntrega"
              :key="item.id"
            >
              <q-item clickable v-ripple @click="clickAdjunto(item)">
                <q-item-section>
                  <q-item-label caption>{{ item.name }}</q-item-label>
                  <q-item-label caption>{{ item.type }}</q-item-label>
                </q-item-section>
                <q-item-section avatar>
                  <q-icon color="primary" name="file_download" />
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </q-step>
        <template v-slot:navigation>
          <q-stepper-navigation class="tarjetaAmarilla">
            <div class="row justify-end">
              <q-btn
                color="btnCancelar"
                label="  Cancelar  "
                class="q-ml-sm"
                @click="clicCancelar"
              />
              <q-btn
                v-if="step > 1"
                color="btnVolver"
                @click="$refs.stepper.previous()"
                label="   Volver   "
                class="q-ml-sm"
              />
              <q-btn
                v-if="step == 1"
                @click="$refs.stepper.next()"
                color="btnContinuar"
                label="  Continuar "
                class="q-ml-sm"
                :disable="!indicadorSeleccionado"
              />
              <q-btn
                v-if="step == 2"
                @click="$refs.stepper.next()"
                color="btnContinuar"
                label="  Continuar "
                class="q-ml-sm"
                :disable="!verificadorValor || !verificadorDescripcion"
              />
              <q-btn
                v-if="step == 3"
                @click="submitVerificador"
                color="primary"
                label="Finalizar"
                class="q-ml-sm"
                :disable="!entrega.adjuntosNuevaEntrega"
              />
            </div>
          </q-stepper-navigation>
        </template>
      </q-stepper>
    </div>
    <div v-else>
      <p>
        Esto es muy extraño. Si lees esto, probablemente es un error del sistema
      </p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import Picker from "src/components/Picker.vue";
import PopupCancelarNuevaEntrega from "src/components/PopupCancelarNuevaEntrega.vue";

export default {
  components: {
    Picker,
    PopupCancelarNuevaEntrega,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const entrega = computed(() => store.state.entrega);
    const verificador = computed(() => store.state.verificador);
    const accion = computed(() => store.state.accion);
    const usuario = computed(() => store.state.usuarix);
    const indicadorSeleccionado = ref(null);
    const verificadorValor = ref(null);
    const verificadorDescripcion = ref(null);
    const mostrarPopupCancelar = ref(false);
    const respuestaPopupCancelar = ref("");
    const clickAdjunto = (item) => {
      window.open(item.url);
    };
    const submitVerificador = () => {
      const nuevoVerificador = {
        usuario: usuario.value.usuario.id,
        indicador: indicadorSeleccionado.value.id,
        valor: verificadorValor.value,
        descripcion: verificadorDescripcion.value,
        adjuntos: entrega.value.adjuntosNuevaEntrega,
      };
      store.dispatch("verificador/postVerificador", nuevoVerificador);
    };
    onMounted(() => {
      if (entrega.value.nuevaEntrega) {
        store.dispatch(
          "accion/reqFuncionesPorAccion",
          entrega.value.nuevaEntrega.id
        );
      }
    });
    onUnmounted(() => {
      store.dispatch("verificador/limpiaNuevoVerificador");
      store.dispatch("producto/limpiaNuevoProducto");
      store.dispatch("entrega/limpiaAdjuntos");
    });
    return {
      clickAdjunto,
      verificador,
      entrega,
      accion,
      indicadorSeleccionado,
      verificadorValor,
      verificadorDescripcion,
      mostrarPopupCancelar,
      respuestaPopupCancelar,
      handlerPopupCancelar: (respuesta) => {
        mostrarPopupCancelar.value = false;
        if (respuesta == "guarda") {
          submitVerificador();
          router.push("acciones");
        } else if (respuesta == "sale") {
          router.push("acciones");
        } else {
          // se hace nada
        }
      },
      submitVerificador,
      enviaAlLider: () => {
        store.dispatch("entrega/workflowEnviaAlLider", {
          entrega_id: verificador.value.nuevoVerificador.id,
          entrega_tipo: "verificador",
        });
      },
      step: ref(1),
      clicCancelar: () => {
        if (verificadorDescripcion.value) mostrarPopupCancelar.value = true;
        else
          router.push(
            accion.value.referenciaSubirEntregable == "AccionesPOA"
              ? "acciones"
              : "accionesPMI"
          );
      },
    };
  },
};
</script>
