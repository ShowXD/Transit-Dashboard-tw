export interface ParkingLot {
  id: number
  external_id: string
  name: string
  car_park_type: number | null
  address: string | null
  lat: number | null
  lon: number | null
  total_spaces: number | null
  available_spaces: number | null
  charge_description: string | null
}

export interface RoadSection {
  id: number
  external_id: string
  road_name: string
  section_name: string | null
  lat: number | null
  lon: number | null
  total_spaces: number | null
  available_spaces: number | null
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  skip: number
  limit: number
}

const BASE = '/api/v1'

export async function fetchLots(
  lat?: number,
  lon?: number,
  radiusM = 2000,
): Promise<PaginatedResponse<ParkingLot>> {
  const params = new URLSearchParams({ radius_m: String(radiusM), limit: '200' })
  if (lat !== undefined) params.set('lat', String(lat))
  if (lon !== undefined) params.set('lon', String(lon))
  const res = await fetch(`${BASE}/parking/lots?${params}`)
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json()
}

export async function fetchRoadSections(
  lat?: number,
  lon?: number,
  radiusM = 1000,
): Promise<PaginatedResponse<RoadSection>> {
  const params = new URLSearchParams({ radius_m: String(radiusM), limit: '200' })
  if (lat !== undefined) params.set('lat', String(lat))
  if (lon !== undefined) params.set('lon', String(lon))
  const res = await fetch(`${BASE}/parking/road-sections?${params}`)
  if (!res.ok) throw new Error(`API error ${res.status}`)
  return res.json()
}
