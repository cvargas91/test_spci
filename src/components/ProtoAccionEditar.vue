<template>
  <q-page>
    <div class="q-pa-md q-gutter-md">
      <q-card class="my-card" v-if="!modoEdicion">
        <q-card-section>
          <div class="text-overline">
            Modificado el {{ accion.modificacion }}
          </div>
          <div class="text-h6">
            {{ accion.id_uaysen }} : {{ accion.titulo }}
          </div>
          <div class="text-subtitle1">Objetivo: {{ accion.objetivo }}</div>
          <div class="text-subtitle2">Proyecto: {{ accion.proyecto }}</div>
          <q-card-actions vertical align="right">
            <q-btn
              class="q-mr-sm"
              color="primary"
              icon="edit"
              label=""
              @click="editaInfoBase(accion)"
            />
          </q-card-actions>
        </q-card-section>
      </q-card>
      <q-card class="my-card" v-else>
        <q-card-section>
          <div class="text-h6">
            {{ accion.id_uaysen }} :
            <q-input v-model="editandoAccionTitulo" label="Título" />
          </div>
          <div class="text-subtitle1">
            <q-input v-model="editandoAccionObjetivo" label="Objetivo" />
          </div>
          <div class="text-subtitle2">
            <q-input v-model="editandoAccionProyecto" label="Proyecto" />
          </div>
          <q-card-actions vertical align="right">
            <q-btn
              class="q-mr-sm"
              color="primary"
              icon="done"
              label=""
              @click="submitEdicion()"
            />
          </q-card-actions>
        </q-card-section>
      </q-card>
      <q-list bordered separator class="rounded-borders">
        <q-item-label header>Estrategias</q-item-label>
        <q-item v-if="aniadirEstrategia">
          <ProtoAgregaEstrategia
            :id_accion="accion.id"
            :mostrar="aniadirEstrategia"
            @update:mostrar="aniadirEstrategia = $event"
          />
        </q-item>
        <q-item v-else v-for="item in accion.estrategias" :key="item.id">
          <q-item-section>
            <q-item-label lines="1">{{ item.id_uaysen }}</q-item-label>
            <q-item-label caption lines="2">
              <span class="text-weight-bold">{{ item.tipo }}</span>
              -- {{ item.descripcion }}
            </q-item-label>
          </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                size="sm"
                color="negative"
                icon="delete"
                label=""
                @click="quitarEstrategia(item)"
              />
            </div>
          </q-item-section>
        </q-item>
        <q-item v-if="accion.estrategias && !accion.estrategias.length"
          >No se han relacionado Estrategias</q-item
        >
        <q-item>
          <q-item-section> </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                color="primary"
                size="sm"
                icon="add"
                label=""
                @click="aniadeEstrategia"
              />
            </div>
          </q-item-section>
        </q-item>
      </q-list>
      <q-list bordered separator class="rounded-borders">
        <q-item-label header>Hitos</q-item-label>
        <q-item v-if="aniadirHito">
          <ProtoAgregaHito
            :id_accion="accion.id"
            :mostrar="aniadirHito"
            @update:mostrar="aniadirHito = $event"
          />
        </q-item>
        <q-item
          clickable
          v-else
          v-for="item in accion.proto_hito_set"
          :key="item.id"
          v-ripple
        >
          <q-item-section>
            <q-item-label lines="1">{{ item.nombre }}</q-item-label>
            <q-item-label caption lines="2">
              {{ item.descripcion }}
            </q-item-label>
          </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                size="sm"
                color="primary"
                icon="edit"
                label=""
                @click="editaHito(item.id)"
              />
              <q-btn size="sm" color="negative" icon="delete" label="" />
            </div>
          </q-item-section>
        </q-item>
        <q-item v-if="accion.proto_hito_set && !accion.proto_hito_set.length"
          >No se han registrado Hitos</q-item
        >
        <q-item>
          <q-item-section> </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                color="primary"
                size="sm"
                icon="add"
                label=""
                @click="aniadeHito"
              />
            </div>
          </q-item-section>
        </q-item>
      </q-list>
      <q-list bordered separator class="rounded-borders">
        <q-item-label header>Funciones e indicadores</q-item-label>
        <q-item v-if="aniadirFuncion">
          <ProtoAgregaFuncion
            :id_accion="accion.id"
            :mostrar="aniadirFuncion"
            @update:mostrar="aniadirFuncion = $event"
          />
        </q-item>
        <q-item
          clickable
          v-else
          v-for="item in accion.proto_funcion_set"
          :key="item.id"
          v-ripple
        >
          <q-item-section>
            <q-item-label lines="1">{{ item.nombre }}</q-item-label>
          </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                size="sm"
                color="primary"
                icon="edit"
                label=""
                @click="editaFuncion(item.id)"
              />
              <q-btn size="sm" color="negative" icon="delete" label="" />
            </div>
          </q-item-section>
        </q-item>
        <q-item
          v-if="accion.proto_funcion_set && !accion.proto_funcion_set.length"
          >No se han registrado Funciones</q-item
        >
        <q-item>
          <q-item-section> </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                color="primary"
                size="sm"
                icon="add"
                label=""
                @click="aniadeFuncion"
              />
            </div>
          </q-item-section>
        </q-item>
      </q-list>
      <q-list bordered separator class="rounded-borders">
        <q-item-label header>Medios de Verificación (MDV)</q-item-label>
        <q-item v-if="aniadirMDV">
          <ProtoAgregaMDV
            :id_accion="accion.id"
            :mostrar="aniadirMDV"
            @update:mostrar="aniadirMDV = $event"
          />
        </q-item>
        <q-item
          clickable
          v-else
          v-for="item in accion.proto_mdv_set"
          :key="item.id"
          v-ripple
        >
          <q-item-section>
            <q-item-label lines="1">{{ item.nombre }}</q-item-label>
          </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                size="sm"
                color="primary"
                icon="edit"
                label=""
                @click="editaMDV(item.id)"
              />
              <q-btn size="sm" color="negative" icon="delete" label="" />
            </div>
          </q-item-section>
        </q-item>
        <q-item v-if="accion.proto_mdv_set && !accion.proto_mdv_set.length"
          >No se han registrado Medios De Verificación</q-item
        >
        <q-item>
          <q-item-section> </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                color="primary"
                size="sm"
                icon="add"
                label=""
                @click="aniadeMDV"
              />
            </div>
          </q-item-section>
        </q-item>
      </q-list>
      <q-list bordered separator class="rounded-borders">
        <q-item-label header>Roles de actores involucrados</q-item-label>
        <q-item v-if="aniadirRol">
          <ProtoAgregaRol
            :id_accion="accion.id"
            :mostrar="aniadirRol"
            @update:mostrar="aniadirRol = $event"
          />
        </q-item>
        <q-item>No se han registrado roles de actores</q-item>
        <q-item>
          <q-item-section> </q-item-section>
          <q-item-section side top>
            <div class="q-gutter-xs">
              <q-btn
                color="primary"
                size="sm"
                icon="add"
                label=""
                @click="aniadeRol"
              />
            </div>
          </q-item-section>
        </q-item>
      </q-list>
      <div class="q-gutter-xs">
        <q-btn
          color="negative"
          icon="delete"
          class="q-mr-sm"
          label="Eliminar la propuesta de acción"
          @click="eliminarAccion"
        />
        <q-btn color="btnCancelar" label="Volver" @click="clicCancelar" />
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, toRef } from "vue";
import { useStore } from "vuex";
import ProtoAgregaEstrategia from "src/components/ProtoAgregaEstrategia.vue";
import ProtoAgregaHito from "src/components/ProtoAgregaHito.vue";
import ProtoAgregaFuncion from "src/components/ProtoAgregaFuncion.vue";
import ProtoAgregaMDV from "src/components/ProtoAgregaMDV.vue";
import ProtoAgregaRol from "src/components/ProtoAgregaRol.vue";

export default {
  props: {
    accion: Object,
  },
  components: {
    ProtoAgregaEstrategia,
    ProtoAgregaHito,
    ProtoAgregaFuncion,
    ProtoAgregaMDV,
    ProtoAgregaRol,
  },
  setup(props) {
    const store = useStore();
    const accion = toRef(props, "accion");
    const modoEdicion = ref(false);
    const editandoAccionTitulo = ref(props.accion.titulo);
    const editandoAccionObjetivo = ref(props.accion.objetivo);
    const editandoAccionProyecto = ref(props.accion.proyecto);
    const aniadirEstrategia = ref(false);
    const aniadirHito = ref(false);
    const aniadirFuncion = ref(false);
    const aniadirMDV = ref(false);
    const aniadirRol = ref(false);

    return {
      accion,
      modoEdicion,
      aniadirEstrategia,
      aniadeEstrategia: () => {
        aniadirEstrategia.value = true;
      },
      aniadirHito,
      aniadeHito: () => {
        aniadirHito.value = true;
      },
      aniadirFuncion,
      aniadeFuncion: () => {
        aniadirFuncion.value = true;
      },
      aniadirMDV,
      aniadeMDV: () => {
        aniadirMDV.value = true;
      },
      aniadirRol,
      aniadeRol: () => {
        aniadirRol.value = true;
      },
      editaInfoBase: (accion) => {
        modoEdicion.value = true;
      },
      quitarEstrategia: (item) => {
        if (
          confirm(
            "¿Está segurx que desea quitar la estrategia de la actual acción?"
          )
        )
          store.dispatch("poador/quitaEstrategia", {
            id_accion: props.accion.id,
            id_estrategia: item.id,
          });
      },
      editaHito: (item) => {
        console.log("edita hito");
        console.log(item);
      },
      editaFuncion: (item) => {
        console.log("edita función");
        console.log(item);
      },
      editaMDV: (item) => {
        console.log("edita MDV");
        console.log(item);
      },
      clicCancelar: () => {
        store.dispatch("poador/cancelaEdicion");
      },
      eliminarAccion: () => {
        if (
          confirm("¿Está segurx que desea eliminar esta propuesta de acción?")
        ) {
          store.dispatch("poador/reqEliminaAccion", props.accion.id);
        }
      },
      editandoAccionTitulo,
      editandoAccionObjetivo,
      editandoAccionProyecto,
      submitEdicion: () => {
        store.dispatch("poador/reqActualizaAccion", {
          id: props.accion.id,
          titulo: editandoAccionTitulo.value,
          objetivo: editandoAccionObjetivo.value,
          proyecto: editandoAccionProyecto.value,
        });
        modoEdicion.value = false;
      },
    };
  },
};
</script>
