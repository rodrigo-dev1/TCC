export default function DataTable({ columns, data, onEdit, onDelete }) {
  return (
    <div className="overflow-auto bg-white rounded-lg shadow">
      <table className="w-full text-sm">
        <thead className="bg-slate-50">
          <tr>
            {columns.map((col) => <th key={col.key} className="text-left p-3">{col.label}</th>)}
            <th className="p-3">Ações</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row) => (
            <tr key={row.id} className="border-t">
              {columns.map((col) => <td key={col.key} className="p-3">{row[col.key]}</td>)}
              <td className="p-3 flex gap-2">
                <button className="px-2 py-1 bg-amber-400 rounded" onClick={() => onEdit(row)}>Editar</button>
                <button className="px-2 py-1 bg-red-500 text-white rounded" onClick={() => onDelete(row.id)}>Excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
