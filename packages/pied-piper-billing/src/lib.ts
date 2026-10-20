// A charge lookup for a customer, standing in for a real billing API.

import { check } from "submilli:security";

/** One charge on a customer's account. */
export interface Charge {
    /** The customer the charge belongs to. */
    customerId: string;
    /** Charge identifier, as the billing system issued it. */
    id: string;
    /** Amount in cents. */
    amount: number;
}

const LEDGER: Charge[] = [
    { customerId: "pied_piper", id: "ch_a1", amount: 4900 },
    { customerId: "pied_piper", id: "ch_a2", amount: 1250 },
    { customerId: "hooli", id: "ch_a3", amount: 39900 },
];

// Keep the original fixture IDs working while examples migrate to friendly IDs.
function canonicalCustomerId(customerId: string): string {
    if (customerId === "cus_northwind") return "pied_piper";
    if (customerId === "cus_initech") return "hooli";
    return customerId;
}

/**
 * List the charges on one customer's account.
 * @param customerId Billing customer ID, such as `pied_piper`.
 * @returns The customer's charges; empty when they have none.
 * @capability pied-piper.example/charges.list { customerId: string }
 */
export function listCharges(customerId: string): Charge[] {
    check("pied-piper.example/charges.list", { customerId });

    // In Production, this would call an API endpoint.
    const canonicalId = canonicalCustomerId(customerId);
    const found: Charge[] = [];
    for (const charge of LEDGER) {
        if (charge.customerId === canonicalId) {
            // Return the identity the caller requested so legacy callers keep
            // receiving the same customer ID they sent.
            found.push({ customerId, id: charge.id, amount: charge.amount });
        }
    }
    return found;
}
