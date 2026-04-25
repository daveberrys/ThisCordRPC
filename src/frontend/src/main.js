import { mount } from "svelte";
import "./app.css";
import App from "./App.svelte";

const appRoot = document.getElementById("app");

const app = mount(App, {
  target: appRoot
});

export default app;
