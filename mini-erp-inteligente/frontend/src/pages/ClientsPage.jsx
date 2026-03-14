import CrudPage from './CrudPage'

export default function ClientsPage() {
  return <CrudPage title="Clientes" endpoint="/clients" fields={[['name','Nome'],['email','Email'],['phone','Telefone'],['document','Documento'],['notes','Observações']]} />
}
