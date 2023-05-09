//import { set } from "core-js/core/dict";

export function setNuevoVerificador(state, nuevoVerificador) {
  state.nuevoVerificador = nuevoVerificador;
}

export function setVerificadores(state, verificadores) {
  state.verificadores = verificadores;
}

export function setVerificadoresUPCI(state, verificadores) {
  state.verificadoresUPCI = verificadores;
}

export function setVerificador(state, verificador) {
  state.verificador = verificador;
}

export function setMetaVerificador(state, avance) {
    state.avance = avance;
}