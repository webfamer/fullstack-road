export function formatRole(role) {
  return `role=${role} from ESM`;
}

export default function describe(name, role) {
  return `${name} -> ${formatRole(role)}`;
}
