const { defineConfig } = require("cypress");
const createBundler = require("@bahmutov/cypress-esbuild-preprocessor");
const addCucumberPreprocessorPlugin = require("@badeball/cypress-cucumber-preprocessor").addCucumberPreprocessorPlugin;
const createEsbuildPlugin = require("@badeball/cypress-cucumber-preprocessor/esbuild").createEsbuildPlugin;

module.exports = defineConfig({
  e2e: {
    async setupNodeEvents(on, config) {
      await addCucumberPreprocessorPlugin(on, config);
      on("file:preprocessor", createBundler({
        plugins: [createEsbuildPlugin(config)],
      }));
      return config;
    },
    specPattern: ["cypress/e2e/**/*.cy.js", "cypress/e2e/**/*.feature"],
    stepDefinitions: "cypress/support/step_definitions/**/*.{js,ts}",
    baseUrl: "https://qa.instulearn.com", // Instulearn QA API base URL
  },
  env: {
    adminEmail: "162.admin@instulearn.com", // Instulearn admin email
    adminPassword: "162162162", // Instulearn admin password
    invalidToken: "invalid_token_here" // Geçersiz token
  }
});
