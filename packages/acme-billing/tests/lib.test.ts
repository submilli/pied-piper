import { label } from "submilli:test";
import { listCharges } from "@submilli/acme-billing";

function main(): void {
    label("lists a customer's own charges");
    const charges = listCharges("pied_piper");
    assert(charges.length === 2, "pied_piper has two charges in the fixture");
    assert(charges[0].customerId === "pied_piper", "friendly result keeps the requested ID");
    assert(charges[0].amount === 4900, "the first is the 4900-cent charge");

    label("scopes the lookup to the customer asked for");
    assert(listCharges("hooli").length === 1, "hooli has one charge");
    assert(listCharges("hooli")[0].customerId === "hooli", "the denied customer remains distinct");
    assert(listCharges("cus_unknown").length === 0, "an unknown customer has none");

    label("keeps legacy customer IDs as compatible aliases");
    const legacyNorthwind = listCharges("cus_northwind");
    assert(legacyNorthwind.length === 2, "cus_northwind still has two charges");
    assert(legacyNorthwind[0].customerId === "cus_northwind", "legacy result keeps the old ID");
    const legacyInitech = listCharges("cus_initech");
    assert(legacyInitech.length === 1, "cus_initech still has one charge");
    assert(legacyInitech[0].customerId === "cus_initech", "legacy denied customer keeps the old ID");
}
