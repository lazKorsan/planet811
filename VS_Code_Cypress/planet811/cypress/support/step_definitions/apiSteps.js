import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import apiHelpers from "../../support/apiHelpers";

Given("I am authenticated as admin", function() {
  return apiHelpers.setUpApi("admin");
});

When("I send GET request to {string}", (endpoint) => {
  apiHelpers.get(endpoint).as("response");
});

Then("response status should be {int}", (statusCode) => {
  cy.get("@response").then(response => {
    apiHelpers.assertStatusCode(response, statusCode);
  });
});